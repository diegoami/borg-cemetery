"""Raw evidence imports fail on corruption, unsafe paths, or omitted deaths."""
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from retain_incident_artifact import retain


def fixture(root,extra=None,dead=False):
    entries={'harvest/harvest.json':json.dumps({'attempts':[{'id':'one','summary':{'dead':True}}] if dead else []}).encode()}
    entries.update(extra or {})
    stream=io.BytesIO()
    with tarfile.open(fileobj=stream,mode='w:gz') as t:
        for name,data in entries.items():
            member=tarfile.TarInfo(name);member.size=len(data);t.addfile(member,io.BytesIO(data))
    path=root/'artifact.zip'
    with zipfile.ZipFile(path,'w') as z:z.writestr('harvest-class-0.tgz',stream.getvalue())
    return path,{'digest':'sha256:'+hashlib.sha256(path.read_bytes()).hexdigest()}


class RetainTest(unittest.TestCase):
    def test_preserve_original_zip_and_small_attempt_journals(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=Path(tmp);archive,metadata=fixture(r,{'harvest/completed/one.json':b'{"status":"stopped"}'})
            original=archive.read_bytes();result=retain(archive,metadata,r/'out')
            self.assertEqual(archive.read_bytes(),original)
            self.assertEqual((r/'out/completed/one.json').read_bytes(),b'{"status":"stopped"}')
            self.assertFalse(result['independent_life'])

    def test_refuse_modified_original_zip(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=Path(tmp);archive,metadata=fixture(r);metadata['digest']='sha256:'+'0'*64
            with self.assertRaisesRegex(ValueError,'digest'):retain(archive,metadata,r/'out')

    def test_refuse_unsafe_tar_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=Path(tmp);archive,metadata=fixture(r,{'harvest/../escape':b'bad'})
            with self.assertRaisesRegex(ValueError,'unsafe'):retain(archive,metadata,r/'out')
            self.assertFalse((r/'escape').exists())

    def test_every_natural_death_requires_packet_even_if_unselected(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=Path(tmp);archive,metadata=fixture(r,dead=True)
            with self.assertRaisesRegex(ValueError,'natural death missing'):retain(archive,metadata,r/'out')
