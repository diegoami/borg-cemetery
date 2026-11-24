# Cemetery statistics

Death-archive statistics, separated by registry and exact retained build. These are selected death records, not a complete sample of games. **No mortality or survival rate is calculated.**

## Archive coverage

| Registry | Dossiers | Known start families | Missing family | Retained attempts | Explicit repeats | Build groups |
| --- | --- | --- | --- | --- | --- | --- |
| [cemetery](sources/cemetery.md) | 324 | 324 | 0 | 332 | 8 | 35 |
| [reborn-historical](sources/reborn-historical.md) | 2378 | 2375 | 0 | 2378 | 0 | 114 |

Shared declared/qualified family keys across registry pairs: **1**. Registry totals are not pooled into an independent-birth count. Different family keys do not prove unrelated births.

A dossier is one retained case. Start families group declared/qualified starting conditions; saved games, verification repeats, human continuations and tuning trials do not become new births. Terminal distributions below weight dossiers, including multiple dossiers of one family.

[Retained extra attempts](attempts.md) lists repeats and unclassified/alternative attempt roles separately. Scenario and human-play outcomes remain in their original reports and are excluded from death distributions.

## Patterns among retained deaths

### cemetery

| Cause | Dossiers |
| --- | --- |
| a crow | 36 |
| poison | 32 |
| a wild cat | 27 |
| a grey mushroom patch | 24 |
| Fang, Farmer Maggot's Dog | 23 |

| Metric | Known records | Minimum | Median | Mean | Maximum |
| --- | --- | --- | --- | --- | --- |
| turn | 324 | 160 | 13394.5 | 39693.29 | 1094860 |
| depth | 299 | 0 | 1 | 1.33 | 18 |
| level | 299 | 1 | 2 | 2.90 | 12 |

### reborn-historical

| Cause | Dossiers |
| --- | --- |
| starvation | 211 |
| Grip, Farmer Maggot's Dog | 155 |
| a small kobold | 141 |
| a giant white mouse | 132 |
| Fang, Farmer Maggot's Dog | 130 |

| Metric | Known records | Minimum | Median | Mean | Maximum |
| --- | --- | --- | --- | --- | --- |
| turn | 2378 | 81 | 7409.5 | 20545.92 | 99880 |
| depth | 2378 | 0 | 1 | 1.29 | 20 |
| level | 2378 | 1 | 1 | 1.55 | 13 |

## Builds

A build group uses project, commit, source-input hash, executable hash, implementation and dirtiness flags. Different binaries at the same commit stay separate. Missing provenance is printed as Unknown; a dirty build must not be treated as the pristine named commit. Profiles are reported separately on each build page.

### cemetery

| Build / source commit | Implementation | Input dirtiness | Dossiers | Start families | Median death turn | Median depth |
| --- | --- | --- | --- | --- | --- | --- |
| [borg-reborn-rs · 3b4924ba366e · 234ea4bdf19cb27b](builds/borg-reborn-rs-3b4924ba366e-234ea4bdf19cb27b/README.md) | rust | no | 39 | 39 | 7990 | 1 |
| [borg-reborn-rs · 8a0b57c85700 · 712f39941f78eada](builds/borg-reborn-rs-8a0b57c85700-712f39941f78eada/README.md) | rust | no | 38 | 38 | 30749 | 1 |
| [borg-reborn-rs · e8b3acfdcfa5 · 08b47ead74bfc439](builds/borg-reborn-rs-e8b3acfdcfa5-08b47ead74bfc439/README.md) | rust | no | 29 | 29 | 12281 | 1 |
| [borg-reborn-rs · 9085c2665c04 · c27d9368e102ea5b](builds/borg-reborn-rs-9085c2665c04-c27d9368e102ea5b/README.md) | rust | no | 28 | 28 | 8687 | 1 |
| [borg-reborn-rs · 1c07181217a7 · 053bb92b0fdbe836](builds/borg-reborn-rs-1c07181217a7-053bb92b0fdbe836/README.md) | rust | no | 27 | 27 | 18142 | 1 |
| [borg-reborn-rs · ab775d488a97 · be7c6e4509e4e065](builds/borg-reborn-rs-ab775d488a97-be7c6e4509e4e065/README.md) | rust | no | 22 | 22 | 48935.5 | 1 |
| [borg-reborn-rs · 206cf4e76908 · 37c190b80bf501a1](builds/borg-reborn-rs-206cf4e76908-37c190b80bf501a1/README.md) | rust | no | 20 | 20 | 9793 | 1 |
| [borg-reborn-rs · 4ecb93d77c62 · b6a5b2d5ad3988b9](builds/borg-reborn-rs-4ecb93d77c62-b6a5b2d5ad3988b9/README.md) | rust | no | 18 | 18 | 19566 | 1 |
| [better-borg-c · 5cd2258dd78d · 5cfaf4ffdf517310](builds/better-borg-c-5cd2258dd78d-5cfaf4ffdf517310/README.md) | Unknown | Unknown | 15 | 15 | 46642 | Unknown |
| [borg-reborn-rs · fde8025a6dfa · f49bf965f68090f5](builds/borg-reborn-rs-fde8025a6dfa-f49bf965f68090f5/README.md) | rust | no | 12 | 12 | 4996 | 1 |
| [borg-reborn-rs · 4d83dd26ef6b · e7b9c44f27fca690](builds/borg-reborn-rs-4d83dd26ef6b-e7b9c44f27fca690/README.md) | rust | no | 11 | 11 | 33735 | 1 |
| [borg-reborn-rs · da097a764239 · a8672f2a76a8563b](builds/borg-reborn-rs-da097a764239-a8672f2a76a8563b/README.md) | rust | no | 11 | 11 | 5297 | 1 |
| [borg-reborn-rs · d8edf54655d8 · 275d43770144db32](builds/borg-reborn-rs-d8edf54655d8-275d43770144db32/README.md) | rust | no | 10 | 10 | 7188 | 1 |
| [borg-reborn-rs · 7f8c6b80a617 · a8e5190bb68504b0](builds/borg-reborn-rs-7f8c6b80a617-a8e5190bb68504b0/README.md) | rust | no | 9 | 9 | 62965 | 1 |
| [better-borg-c · 867c777845fd · 53cf9896b1c37b5e](builds/better-borg-c-867c777845fd-53cf9896b1c37b5e/README.md) | Unknown | Unknown | 5 | 5 | 27770 | Unknown |
| [borg-reborn-rs · e5cc54697cf5 · 91efad63f300e348](builds/borg-reborn-rs-e5cc54697cf5-91efad63f300e348/README.md) | rust | no | 4 | 4 | 5100 | 0 |
| [borg-rs · f772eb6dcb93 · 4190bcfe4490dd59](builds/borg-rs-f772eb6dcb93-4190bcfe4490dd59/README.md) | rust | yes | 4 | 4 | 5915.5 | 1 |
| [better-borg-c · 1cd426af4848 · 140e093e023497bc](builds/better-borg-c-1cd426af4848-140e093e023497bc/README.md) | Unknown | Unknown | 2 | 2 | 112464 | Unknown |
| [borg-reborn-rs · 103b50a4b7f6 · b293e1e65c7f1ae5](builds/borg-reborn-rs-103b50a4b7f6-b293e1e65c7f1ae5/README.md) | rust | no | 2 | 2 | 34021.5 | 1.5 |
| [borg-reborn-rs · 6cd5c8bf8245 · 36c4bcd3e05292c4](builds/borg-reborn-rs-6cd5c8bf8245-36c4bcd3e05292c4/README.md) | rust | no | 2 | 2 | 8567 | 1 |
| [borg-reborn-rs · f02cd2940a74 · dd041c611ca31f4a](builds/borg-reborn-rs-f02cd2940a74-dd041c611ca31f4a/README.md) | rust | no | 2 | 2 | 42460.5 | 1 |
| [better-borg-c · 22f817c96843 · 56d66261cfdedc8a](builds/better-borg-c-22f817c96843-56d66261cfdedc8a/README.md) | Unknown | Unknown | 1 | 1 | 179053 | Unknown |
| [better-borg-c · 2cebef1b0f39 · ac0538b9d41fc2dd](builds/better-borg-c-2cebef1b0f39-ac0538b9d41fc2dd/README.md) | Unknown | Unknown | 1 | 1 | 73100 | Unknown |
| [better-borg-c · 5c23742ced30 · 6b9c9e1452a9173e](builds/better-borg-c-5c23742ced30-6b9c9e1452a9173e/README.md) | Unknown | Unknown | 1 | 1 | 10940 | Unknown |
| [borg-reborn-rs · 08631d514134 · cc3e21278f3800b0](builds/borg-reborn-rs-08631d514134-cc3e21278f3800b0/README.md) | rust | no | 1 | 1 | 3640 | 1 |
| [borg-reborn-rs · 7f8c6b80a617 · 3316a68f0837207c](builds/borg-reborn-rs-7f8c6b80a617-3316a68f0837207c/README.md) | rust | yes | 1 | 1 | 96820 | 2 |
| [borg-reborn-rs · 7f8c6b80a617 · d934f693cb16bae9](builds/borg-reborn-rs-7f8c6b80a617-d934f693cb16bae9/README.md) | rust | yes | 1 | 1 | 97710 | 2 |
| [borg-reborn-rs · 800cf9569d4f · fcd1cfd63e4ceff2](builds/borg-reborn-rs-800cf9569d4f-fcd1cfd63e4ceff2/README.md) | rust | yes | 1 | 1 | 37759 | 1 |
| [borg-reborn-rs · 8a427494fa3c · 2188d039a471e09c](builds/borg-reborn-rs-8a427494fa3c-2188d039a471e09c/README.md) | rust | no | 1 | 1 | 86224 | 1 |
| [borg-reborn-rs · c7ea18dff9f1 · 56f2830db3f69485](builds/borg-reborn-rs-c7ea18dff9f1-56f2830db3f69485/README.md) | rust | no | 1 | 1 | 174601 | 2 |
| [borg-reborn-rs · cfd011a6b2ff · 2b9ae8beec943964](builds/borg-reborn-rs-cfd011a6b2ff-2b9ae8beec943964/README.md) | rust | no | 1 | 1 | 11412 | 1 |
| [borg-reborn-rs · d8b55d647ec9 · ea2900d6330878e8](builds/borg-reborn-rs-d8b55d647ec9-ea2900d6330878e8/README.md) | rust | no | 1 | 1 | 77923 | 1 |
| [borg-reborn-rs · e9a6a521f3ac · 4cc9e5cf7c6e07ad](builds/borg-reborn-rs-e9a6a521f3ac-4cc9e5cf7c6e07ad/README.md) | rust | no | 1 | 1 | 3640 | 1 |
| [borg-rs · 9881301ceaad · 1948f6a957e27770](builds/borg-rs-9881301ceaad-1948f6a957e27770/README.md) | rust | no | 1 | 1 | 36289 | 1 |
| [borg-rs · aa4ad6cfeea2 · 24bf8fb260989224](builds/borg-rs-aa4ad6cfeea2-24bf8fb260989224/README.md) | rust | no | 1 | 1 | 22841 | 1 |

### reborn-historical

| Build / source commit | Implementation | Input dirtiness | Dossiers | Start families | Median death turn | Median depth |
| --- | --- | --- | --- | --- | --- | --- |
| [borg-reborn-rs · 6491ea0fa28b · c97366af4f836250](builds/borg-reborn-rs-6491ea0fa28b-c97366af4f836250/README.md) | rust | yes | 50 | 50 | 3554 | 1 |
| [borg-reborn-rs · 155c25aae6ba · 5d050a5d16bf25b3](builds/borg-reborn-rs-155c25aae6ba-5d050a5d16bf25b3/README.md) | rust | no | 48 | 48 | 2897.5 | 1 |
| [borg-reborn-rs · 3bffe5847046 · 38ac8df762c0509b](builds/borg-reborn-rs-3bffe5847046-38ac8df762c0509b/README.md) | rust | no | 48 | 48 | 2843.5 | 1 |
| [borg-reborn-rs · 9644204b66b6 · 01721f46ef1eae7a](builds/borg-reborn-rs-9644204b66b6-01721f46ef1eae7a/README.md) | rust | no | 48 | 48 | 2654 | 1 |
| [borg-reborn-rs · f2b2e1616a4f · 8e3ab5f29d05b44d](builds/borg-reborn-rs-f2b2e1616a4f-8e3ab5f29d05b44d/README.md) | rust | no | 48 | 48 | 2915 | 1 |
| [borg-reborn-rs · 4402f1241990 · c154ae309db68621](builds/borg-reborn-rs-4402f1241990-c154ae309db68621/README.md) | rust | no | 47 | 47 | 6650 | 1 |
| [borg-reborn-rs · 6318cd2b8271 · b01184874d664361](builds/borg-reborn-rs-6318cd2b8271-b01184874d664361/README.md) | rust | no | 47 | 47 | 1492 | 1 |
| [borg-reborn-rs · 9124a2b0c52c · 53e27510744956eb](builds/borg-reborn-rs-9124a2b0c52c-53e27510744956eb/README.md) | rust | no | 47 | 47 | 21280 | 1 |
| [borg-reborn-rs · 03a7b8e2f5cf · 18ceacc8f075d056](builds/borg-reborn-rs-03a7b8e2f5cf-18ceacc8f075d056/README.md) | rust | no | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · 1137bfee88c7 · a3c640b45ac081c7](builds/borg-reborn-rs-1137bfee88c7-a3c640b45ac081c7/README.md) | rust | no | 46 | 46 | 4235 | 1 |
| [borg-reborn-rs · 1a7b9e3e1f20 · b6ccdc8ed38b92cc](builds/borg-reborn-rs-1a7b9e3e1f20-b6ccdc8ed38b92cc/README.md) | rust | yes | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · 384eba93097a · 6237b2d2198e48fa](builds/borg-reborn-rs-384eba93097a-6237b2d2198e48fa/README.md) | rust | yes | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · 452ec40e2d7e · cea039c95eb1e2a8](builds/borg-reborn-rs-452ec40e2d7e-cea039c95eb1e2a8/README.md) | rust | yes | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · 630a2f48ef9e · fcf06ff5b44503b6](builds/borg-reborn-rs-630a2f48ef9e-fcf06ff5b44503b6/README.md) | rust | no | 46 | 46 | 4235 | 1 |
| [borg-reborn-rs · 83f6799f7943 · d4c31854fe381271](builds/borg-reborn-rs-83f6799f7943-d4c31854fe381271/README.md) | rust | yes | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · 851a1e23990a · 64e58077827dead1](builds/borg-reborn-rs-851a1e23990a-64e58077827dead1/README.md) | rust | yes | 46 | 46 | 4235 | 1 |
| [borg-reborn-rs · 8f5e6313f9a4 · 2cf2c56961399894](builds/borg-reborn-rs-8f5e6313f9a4-2cf2c56961399894/README.md) | rust | yes | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · 96f5fd0e3620 · d9a322edbd4fb415](builds/borg-reborn-rs-96f5fd0e3620-d9a322edbd4fb415/README.md) | rust | no | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · 991e0fe41560 · 9b1ded6e335453bc](builds/borg-reborn-rs-991e0fe41560-9b1ded6e335453bc/README.md) | rust | yes | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · 9a4757481dac · 64f0861d4c682bf2](builds/borg-reborn-rs-9a4757481dac-64f0861d4c682bf2/README.md) | rust | yes | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · 9d3a6583a74d · dd46ee2d4778270e](builds/borg-reborn-rs-9d3a6583a74d-dd46ee2d4778270e/README.md) | rust | no | 46 | 46 | 4235 | 1 |
| [borg-reborn-rs · 9e8c7ec068d2 · fd57f6d12ad4ddc1](builds/borg-reborn-rs-9e8c7ec068d2-fd57f6d12ad4ddc1/README.md) | rust | yes | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · a4b37e7fed36 · 71898c90634273fc](builds/borg-reborn-rs-a4b37e7fed36-71898c90634273fc/README.md) | rust | no | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · a4b58da63771 · 16f065391b933eb1](builds/borg-reborn-rs-a4b58da63771-16f065391b933eb1/README.md) | rust | no | 46 | 46 | 4235 | 1 |
| [borg-reborn-rs · ae1e60192944 · 65aa9db9a2dc6055](builds/borg-reborn-rs-ae1e60192944-65aa9db9a2dc6055/README.md) | rust | no | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · c7a3bc7f8e82 · 70624cc687f204d8](builds/borg-reborn-rs-c7a3bc7f8e82-70624cc687f204d8/README.md) | rust | no | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · e1218a07a6a9 · d93ed8e25566121d](builds/borg-reborn-rs-e1218a07a6a9-d93ed8e25566121d/README.md) | rust | no | 46 | 46 | 4235 | 1 |
| [borg-reborn-rs · ec96636d1493 · 4b7ea47477ceeb72](builds/borg-reborn-rs-ec96636d1493-4b7ea47477ceeb72/README.md) | rust | no | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · fd894e05e344 · f30c7699aaf639d8](builds/borg-reborn-rs-fd894e05e344-f30c7699aaf639d8/README.md) | rust | yes | 46 | 46 | 4874 | 1 |
| [borg-reborn-rs · 381b0212ee9e · 25f1be92c27a1d12](builds/borg-reborn-rs-381b0212ee9e-25f1be92c27a1d12/README.md) | rust | yes | 45 | 45 | 3811 | 1 |
| [borg-reborn-rs · 795a3bfb1c5c · f384b1f31759e56e](builds/borg-reborn-rs-795a3bfb1c5c-f384b1f31759e56e/README.md) | rust | yes | 45 | 45 | 1535 | 1 |
| [borg-reborn-rs · 66aff7999c28 · c347a576001ed0de](builds/borg-reborn-rs-66aff7999c28-c347a576001ed0de/README.md) | rust | yes | 41 | 41 | 22980 | 1 |
| [borg-reborn-rs · 97bbe79f8151 · 5307bc32e9c4fb55](builds/borg-reborn-rs-97bbe79f8151-5307bc32e9c4fb55/README.md) | rust | no | 36 | 36 | 10233 | 1 |
| [borg-reborn-rs · bd249a207ccd · 35aea3aaf1acd000](builds/borg-reborn-rs-bd249a207ccd-35aea3aaf1acd000/README.md) | rust | no | 36 | 36 | 5226 | 1 |
| [borg-reborn-rs · 315fa05c6dc4 · 659aa8c0616f2ed8](builds/borg-reborn-rs-315fa05c6dc4-659aa8c0616f2ed8/README.md) | rust | no | 33 | 33 | 26921 | 1 |
| [borg-reborn-rs · 5e286dbf81e7 · af932fe699d85e51](builds/borg-reborn-rs-5e286dbf81e7-af932fe699d85e51/README.md) | rust | no | 33 | 33 | 30740 | 1 |
| [borg-reborn-rs · 809b8bda3a7e · f0df5611ef67a572](builds/borg-reborn-rs-809b8bda3a7e-f0df5611ef67a572/README.md) | rust | no | 32 | 32 | 25846 | 1 |
| [borg-reborn-rs · d38accaccf24 · c096eb0501b93c50](builds/borg-reborn-rs-d38accaccf24-c096eb0501b93c50/README.md) | rust | yes | 32 | 32 | 3316.5 | 1 |
| [borg-reborn-rs · dae0d086c015 · 5842b69a0c189bdd](builds/borg-reborn-rs-dae0d086c015-5842b69a0c189bdd/README.md) | rust | no | 28 | 28 | 26347.5 | 1 |
| [borg-reborn-rs · d4cde78fd36c · 9ab1b2f12ae16522](builds/borg-reborn-rs-d4cde78fd36c-9ab1b2f12ae16522/README.md) | rust | no | 24 | 24 | 23184.5 | 1 |
| [borg-reborn-rs · d106510a3471 · 56cf0de1f3ec54de](builds/borg-reborn-rs-d106510a3471-56cf0de1f3ec54de/README.md) | rust | no | 22 | 22 | 36625.5 | 1 |
| [borg-reborn-rs · e2575fc07a15 · 3db8925f813d7c73](builds/borg-reborn-rs-e2575fc07a15-3db8925f813d7c73/README.md) | rust | no | 22 | 22 | 8392.5 | 1 |
| [borg-reborn-rs · 3a3d36d5a2d1 · 4d6b552755169acc](builds/borg-reborn-rs-3a3d36d5a2d1-4d6b552755169acc/README.md) | c-bbc-m7 | no | 16 | 16 | 25167.5 | 1 |
| [borg-reborn-rs · 5211e752b181 · 339d2714502e7ca8](builds/borg-reborn-rs-5211e752b181-339d2714502e7ca8/README.md) | rust | no | 16 | 16 | 8648 | 1 |
| [borg-reborn-rs · 690ae98a53c9 · 77ff0331746c2053](builds/borg-reborn-rs-690ae98a53c9-77ff0331746c2053/README.md) | rust | no | 16 | 16 | 8648 | 1 |
| [borg-reborn-rs · 7570d10aad14 · 912ba5c7f5281010](builds/borg-reborn-rs-7570d10aad14-912ba5c7f5281010/README.md) | rust | no | 16 | 16 | 8648 | 1 |
| [borg-reborn-rs · dcd4f65c34f5 · 16d86b68badc1b75](builds/borg-reborn-rs-dcd4f65c34f5-16d86b68badc1b75/README.md) | rust | no | 16 | 16 | 8648 | 1 |
| [borg-reborn-rs · ddeea81fbe02 · 7a5aac3625a2a3c6](builds/borg-reborn-rs-ddeea81fbe02-7a5aac3625a2a3c6/README.md) | rust | no | 16 | 16 | 8648 | 1 |
| [borg-reborn-rs · faee99a31cbb · ca00943be09c33bc](builds/borg-reborn-rs-faee99a31cbb-ca00943be09c33bc/README.md) | rust | no | 16 | 16 | 8648 | 1 |
| [borg-reborn-rs · 2d8673b766c3 · 9ea3874520183053](builds/borg-reborn-rs-2d8673b766c3-9ea3874520183053/README.md) | rust | no | 15 | 15 | 8008 | 1 |
| [borg-reborn-rs · 382123bc4a65 · 30c12d003aa80c1b](builds/borg-reborn-rs-382123bc4a65-30c12d003aa80c1b/README.md) | rust | no | 15 | 15 | 8008 | 1 |
| [borg-reborn-rs · 3a3d36d5a2d1 · ea694bf75837581e](builds/borg-reborn-rs-3a3d36d5a2d1-ea694bf75837581e/README.md) | c-pristine | no | 15 | 15 | 7367 | 1 |
| [borg-reborn-rs · 798239ad4644 · 946f05a17d60cb6d](builds/borg-reborn-rs-798239ad4644-946f05a17d60cb6d/README.md) | rust | no | 15 | 15 | 8008 | 1 |
| [borg-reborn-rs · c7a3bc7f8e82 · b50bb9b3ea9982b6](builds/borg-reborn-rs-c7a3bc7f8e82-b50bb9b3ea9982b6/README.md) | c-pristine | no | 15 | 15 | 7367 | 1 |
| [borg-reborn-rs · da71d0542980 · 561e46a3a6a42ac4](builds/borg-reborn-rs-da71d0542980-561e46a3a6a42ac4/README.md) | rust | no | 15 | 15 | 8008 | 1 |
| [borg-reborn-rs · ea6c91678d30 · a428a6a5a73a3b35](builds/borg-reborn-rs-ea6c91678d30-a428a6a5a73a3b35/README.md) | c | no | 15 | 15 | 15117 | 1 |
| [borg-reborn-rs · eb43cfe8c644 · 9dbaffc93c9e68d2](builds/borg-reborn-rs-eb43cfe8c644-9dbaffc93c9e68d2/README.md) | rust | no | 15 | 15 | 12805 | 1 |
| [borg-reborn-rs · e6d13fc9baff · ae98c3ff3475d575](builds/borg-reborn-rs-e6d13fc9baff-ae98c3ff3475d575/README.md) | rust | no | 14 | 12 | 23165.5 | 1 |
| [borg-reborn-rs · 3075dae91758 · cae50d96ec0fb9e4](builds/borg-reborn-rs-3075dae91758-cae50d96ec0fb9e4/README.md) | rust | no | 12 | 12 | 10777 | 1 |
| [borg-reborn-rs · 30ab9d664403 · 2925e7fc77be9e9e](builds/borg-reborn-rs-30ab9d664403-2925e7fc77be9e9e/README.md) | rust | yes | 12 | 12 | 15194.5 | 1 |
| [borg-reborn-rs · 3de87e3ee39c · 0165c03a9478b7a5](builds/borg-reborn-rs-3de87e3ee39c-0165c03a9478b7a5/README.md) | rust | no | 12 | 12 | 15194.5 | 1 |
| [borg-reborn-rs · 5d9abb8f5c16 · deff7f38ce3f3ce6](builds/borg-reborn-rs-5d9abb8f5c16-deff7f38ce3f3ce6/README.md) | rust | yes | 12 | 12 | 10777 | 1 |
| [borg-reborn-rs · 726e04fa9d01 · 2bd6d8a8e58b692a](builds/borg-reborn-rs-726e04fa9d01-2bd6d8a8e58b692a/README.md) | rust | yes | 12 | 12 | 15194.5 | 1 |
| [borg-reborn-rs · 9f854b458b90 · c61c2a68eb525f7c](builds/borg-reborn-rs-9f854b458b90-c61c2a68eb525f7c/README.md) | rust | yes | 12 | 12 | 10777 | 1 |
| [borg-reborn-rs · a45b434e4427 · 3d578edf9a3b4cbe](builds/borg-reborn-rs-a45b434e4427-3d578edf9a3b4cbe/README.md) | rust | yes | 12 | 12 | 10777 | 1 |
| [borg-reborn-rs · b7f865d32487 · 47c6a49194f925c4](builds/borg-reborn-rs-b7f865d32487-47c6a49194f925c4/README.md) | rust | yes | 12 | 12 | 15455 | 1 |
| [borg-reborn-rs · 251d39c41f8e · 5821ade5e940da7c](builds/borg-reborn-rs-251d39c41f8e-5821ade5e940da7c/README.md) | rust | yes | 11 | 11 | 12007 | 1 |
| [borg-reborn-rs · 25a6805bb5c7 · 1fa840056f96d40d](builds/borg-reborn-rs-25a6805bb5c7-1fa840056f96d40d/README.md) | rust | no | 11 | 11 | 12007 | 1 |
| [borg-reborn-rs · 2f969dfbddf5 · d234e0ba0ea6447d](builds/borg-reborn-rs-2f969dfbddf5-d234e0ba0ea6447d/README.md) | rust | no | 11 | 11 | 6367 | 1 |
| [borg-reborn-rs · 30ab9d664403 · b21ca276be41437a](builds/borg-reborn-rs-30ab9d664403-b21ca276be41437a/README.md) | rust | yes | 11 | 11 | 12007 | 1 |
| [borg-reborn-rs · 46e1e3c69c8d · 9512e52896766a1c](builds/borg-reborn-rs-46e1e3c69c8d-9512e52896766a1c/README.md) | rust | no | 11 | 11 | 8008 | 1 |
| [borg-reborn-rs · 5d9abb8f5c16 · cf141b1805232992](builds/borg-reborn-rs-5d9abb8f5c16-cf141b1805232992/README.md) | rust | yes | 11 | 11 | 12007 | 1 |
| [borg-reborn-rs · 66aff7999c28 · eae6118b2ee6e11c](builds/borg-reborn-rs-66aff7999c28-eae6118b2ee6e11c/README.md) | rust | no | 11 | 11 | 12007 | 1 |
| [borg-reborn-rs · 6a6e6b735987 · 69300562ef75c5e8](builds/borg-reborn-rs-6a6e6b735987-69300562ef75c5e8/README.md) | rust | no | 11 | 11 | 12007 | 1 |
| [borg-reborn-rs · 8bdd9c97c87e · 2eb9cf01fa6acf9c](builds/borg-reborn-rs-8bdd9c97c87e-2eb9cf01fa6acf9c/README.md) | rust | no | 11 | 11 | 7912 | 1 |
| [borg-reborn-rs · 99278776cdcb · ce7fcb8bd381aa37](builds/borg-reborn-rs-99278776cdcb-ce7fcb8bd381aa37/README.md) | rust | no | 11 | 11 | 12007 | 1 |
| [borg-reborn-rs · 132aeb26a54a · 8614339ff6f97d65](builds/borg-reborn-rs-132aeb26a54a-8614339ff6f97d65/README.md) | rust | no | 10 | 10 | 14225 | 1 |
| [borg-reborn-rs · 30ab9d664403 · c1cfbb01c56f06d3](builds/borg-reborn-rs-30ab9d664403-c1cfbb01c56f06d3/README.md) | rust | yes | 8 | 8 | 20905.5 | 1 |
| [borg-reborn-rs · 3c830cebf704 · 1bee2c76dd36da9a](builds/borg-reborn-rs-3c830cebf704-1bee2c76dd36da9a/README.md) | rust | no | 8 | 8 | 4732.5 | 1 |
| [borg-reborn-rs · 726e04fa9d01 · 2df5f8b685040f1b](builds/borg-reborn-rs-726e04fa9d01-2df5f8b685040f1b/README.md) | rust | yes | 8 | 8 | 20905.5 | 1 |
| [borg-reborn-rs · 726e04fa9d01 · 4d0c0bd43e342231](builds/borg-reborn-rs-726e04fa9d01-4d0c0bd43e342231/README.md) | rust | no | 8 | 8 | 20905.5 | 1 |
| [borg-reborn-rs · 8dd52e1ed52e · 83029d28d797ee7d](builds/borg-reborn-rs-8dd52e1ed52e-83029d28d797ee7d/README.md) | rust | no | 6 | 6 | 8941.5 | 1 |
| [borg-reborn-rs · a692a8b43bc5 · 6bd29643850ccfaf](builds/borg-reborn-rs-a692a8b43bc5-6bd29643850ccfaf/README.md) | rust | no | 6 | 6 | 8941.5 | 1 |
| [borg-reborn-rs · a74a446c09ce · 6746bcc0edaa21c4](builds/borg-reborn-rs-a74a446c09ce-6746bcc0edaa21c4/README.md) | rust | no | 6 | 6 | 6485.5 | 1 |
| [borg-reborn-rs · a9210a39e09e · 1f18ac09df3acfbf](builds/borg-reborn-rs-a9210a39e09e-1f18ac09df3acfbf/README.md) | rust | no | 6 | 6 | 2814.5 | 1 |
| [borg-reborn-rs · c048db9e689d · 6d2330719304974f](builds/borg-reborn-rs-c048db9e689d-6d2330719304974f/README.md) | rust | no | 6 | 6 | 2814.5 | 1 |
| [borg-reborn-rs · c93d0f2385af · 8d7398b38d32a1c3](builds/borg-reborn-rs-c93d0f2385af-8d7398b38d32a1c3/README.md) | rust | no | 6 | 6 | 8941.5 | 1 |
| [borg-reborn-rs · e8b9cb10b071 · 8e61ae233d5bbd28](builds/borg-reborn-rs-e8b9cb10b071-8e61ae233d5bbd28/README.md) | rust | no | 6 | 6 | 6485.5 | 1 |
| [borg-reborn-rs · 4fa37de9730e · e4e8ba20350aa2b2](builds/borg-reborn-rs-4fa37de9730e-e4e8ba20350aa2b2/README.md) | rust | no | 5 | 5 | 15220 | 1 |
| [borg-reborn-rs · 60f953c7b5d0 · 201cb266fcd189fb](builds/borg-reborn-rs-60f953c7b5d0-201cb266fcd189fb/README.md) | rust | no | 5 | 5 | 4841 | 1 |
| [borg-reborn-rs · 9f401cbef492 · fb7b3db6c4a866cf](builds/borg-reborn-rs-9f401cbef492-fb7b3db6c4a866cf/README.md) | rust | no | 5 | 5 | 5078 | 1 |
| [borg-reborn-rs · d7ec6e6c3a26 · 7e7e70659760ab06](builds/borg-reborn-rs-d7ec6e6c3a26-7e7e70659760ab06/README.md) | rust | no | 5 | 5 | 5078 | 1 |
| [borg-reborn-rs · eebbf1904ae1 · 726c45913a61f273](builds/borg-reborn-rs-eebbf1904ae1-726c45913a61f273/README.md) | rust | no | 5 | 5 | 5078 | 1 |
| [borg-reborn-rs · 6d36fe87de12 · 9d25522c5b9b505a](builds/borg-reborn-rs-6d36fe87de12-9d25522c5b9b505a/README.md) | rust | no | 4 | 4 | 4469 | 1 |
| [borg-reborn-rs · 7598d50f1e62 · 2d844c9ad3f055c7](builds/borg-reborn-rs-7598d50f1e62-2d844c9ad3f055c7/README.md) | rust | no | 4 | 4 | 4959.5 | 1 |
| [borg-reborn-rs · 7913bc84e160 · becf968e57484121](builds/borg-reborn-rs-7913bc84e160-becf968e57484121/README.md) | rust | no | 4 | 4 | 4469 | 1 |
| [borg-reborn-rs · 437d7e66da9b · f79a299db6ee65e7](builds/borg-reborn-rs-437d7e66da9b-f79a299db6ee65e7/README.md) | rust | no | 3 | 3 | 1187 | 1 |
| [borg-reborn-rs · 8fe1d1c5353f · 4d63c32ab7d84e36](builds/borg-reborn-rs-8fe1d1c5353f-4d63c32ab7d84e36/README.md) | rust | no | 3 | 3 | 8922 | 1 |
| [borg-reborn-rs · 30ab9d664403 · 884fefaea4b62a19](builds/borg-reborn-rs-30ab9d664403-884fefaea4b62a19/README.md) | rust | yes | 2 | 2 | 6281 | 1 |
| [borg-reborn-rs · 30ab9d664403 · bcb268460b4f3414](builds/borg-reborn-rs-30ab9d664403-bcb268460b4f3414/README.md) | rust | yes | 2 | 2 | 6281 | 1 |
| [borg-reborn-rs · 4c09720d2a75 · 5c86242943d0720c](builds/borg-reborn-rs-4c09720d2a75-5c86242943d0720c/README.md) | rust | no | 2 | 2 | 6281 | 1 |
| [borg-reborn-rs · a794755072a1 · ee0db97daaa1f2b2](builds/borg-reborn-rs-a794755072a1-ee0db97daaa1f2b2/README.md) | rust | yes | 2 | 2 | 6281 | 1 |
| [borg-reborn-rs · bb1a37f87290 · 4a71170bd6a41951](builds/borg-reborn-rs-bb1a37f87290-4a71170bd6a41951/README.md) | rust | no | 2 | 2 | 1433.5 | 1 |
| [borg-reborn-rs · 09bf83dece65 · 7908273ee347cca9](builds/borg-reborn-rs-09bf83dece65-7908273ee347cca9/README.md) | rust | no | 1 | 1 | 3329 | 1 |
| [borg-reborn-rs · 1915f0910d12 · fe324d47c040f6ac](builds/borg-reborn-rs-1915f0910d12-fe324d47c040f6ac/README.md) | rust | yes | 1 | 1 | 18376 | 2 |
| [borg-reborn-rs · 321db9028fb3 · cc745772c8e8cf8b](builds/borg-reborn-rs-321db9028fb3-cc745772c8e8cf8b/README.md) | c | no | 1 | 1 | 7195 | 1 |
| [borg-reborn-rs · 457559ec3d5f · aa7683ece45a0239](builds/borg-reborn-rs-457559ec3d5f-aa7683ece45a0239/README.md) | rust | no | 1 | 1 | 666 | 1 |
| [borg-reborn-rs · 46d0b40e469a · 0148c1613ebae3ad](builds/borg-reborn-rs-46d0b40e469a-0148c1613ebae3ad/README.md) | rust | no | 1 | 1 | 12007 | 17 |
| [borg-reborn-rs · ad7bf0f0646c · 0a3d5d62fb400b62](builds/borg-reborn-rs-ad7bf0f0646c-0a3d5d62fb400b62/README.md) | rust | no | 1 | 1 | 743 | 1 |
| [borg-reborn-rs · b80ed55657bd · a84423d6b31c2c3d](builds/borg-reborn-rs-b80ed55657bd-a84423d6b31c2c3d/README.md) | rust | no | 1 | 1 | 743 | 1 |
| [borg-reborn-rs · eceb5ec5ab80 · 1e5074b63cc06fea](builds/borg-reborn-rs-eceb5ec5ab80-1e5074b63cc06fea/README.md) | rust | no | 1 | 1 | 666 | 1 |
| [borg-reborn-rs · f0eeee25d1ff · e1d34e3b231f92ff](builds/borg-reborn-rs-f0eeee25d1ff-e1d34e3b231f92ff/README.md) | rust | no | 1 | 1 | 666 | 1 |
| [borg-reborn-rs · f71a88a0a310 · 85794ac3606f6b1b](builds/borg-reborn-rs-f71a88a0a310-85794ac3606f6b1b/README.md) | Unknown | Unknown | 1 | 1 | 671 | 1 |
| [borg-reborn-rs · f85fcf421770 · 12daab3633d0e6ad](builds/borg-reborn-rs-f85fcf421770-12daab3633d0e6ad/README.md) | rust | no | 1 | 1 | 3885 | 1 |

## Updating

```bash
python3 scripts/build_statistics.py
python3 scripts/build_statistics.py --check
```

Normal regeneration refreshes the local registry and preserves the explicitly pinned external snapshot. Native death registration also refreshes these reports. To update the external inventory from a clean checkout:

```bash
python3 scripts/build_statistics.py --external-checkout /path/to/borg-reborn-rs --external-ref FULL_COMMIT_SHA
```

The tool reads and hashes records only; it does not execute source tools, copy historical dossiers, or include ignored validation caches. External refreshes must be committed with the reports. Coverage is the direct death registries listed above. Seeded CI batches, all-run denominators and scenario outcomes are not read by this report.
