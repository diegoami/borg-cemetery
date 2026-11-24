#include "obj-desc.h"
#include "player-spell.h"

static struct object *fixture_add(int tval, const char *name, int number)
{
	struct object *obj = object_new();
	struct object_kind *kind = lookup_kind(tval, lookup_sval(tval, name));
	if (!kind) quit_fmt("fixture: unknown kind %s", name);
	object_prep(obj, kind, 0, MINIMISE);
	obj->number = number;
	obj->known = object_new();
	object_set_base_known(player, obj);
	obj->known->notice |= OBJ_NOTICE_ASSESSED;
	inven_carry(player, obj, false, false);
	object_flavor_aware(player, obj);
	player_know_object(player, obj);
	return obj;
}

static void fixture_inventory(FILE *fp)
{
	fprintf(fp, "state\t%ld\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n", (long)turn,
		player->depth, player->lev, player->chp, player->mhp, player->csp,
		player->msp, player->upkeep->inven_cnt);
	for (int i = 0; i < z_info->pack_size; ++i) {
		struct object *obj = player->upkeep->inven[i];
		char name[160];
		if (!obj) continue;
		object_desc(name, sizeof(name), obj, ODESC_FULL, player);
		fprintf(fp, "pack\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%s\n", i,
			obj->number, object_runes_known(obj), obj->origin, obj->origin_depth,
			obj->to_h, obj->to_d, obj->to_a, obj->pval, obj->ego ? obj->ego->eidx : 0, name);
	}
	for (size_t i = 0; i < max_runes(); ++i) {
		if (player_knows_rune(player, i)) fprintf(fp, "rune\t%zu\t%s\n", i, rune_name(i));
	}
}

static void fixture_room(void)
{
	wipe_mon_list(cave, player);
	for (int y = -2; y <= 2; ++y) {
		for (int x = -2; x <= 12; ++x) {
			struct loc grid = loc_sum(player->grid, loc(x, y));
			if (!square_in_bounds_fully(cave, grid))
				quit("fixture: room outside map");
			square_set_feat(cave, grid, FEAT_FLOOR);
			sqinfo_on(square(cave, grid)->info, SQUARE_GLOW);
			square_memorize(cave, grid);
		}
	}
	player->upkeep->update |= PU_UPDATE_VIEW | PU_MONSTERS;
	update_stuff(player);
}

static void fixture_prepare(void)
{
	const char *mode = getenv("CASE_FIXTURE_MODE");
	const char *out = getenv("CASE_FIXTURE_SAVE");
	if (!mode) return;
	if (!streq(mode, "inspect")) {
		if (streq(mode, "mage-book")) {
			if (player->class->cidx != 1 || player->lev != 17) quit("fixture: expected CL17 Mage");
			int index = -1;
			for (int i = 0; i < player->class->magic.total_spells; ++i) {
				if (streq(spell_by_index(player, i)->name, "Identify Rune")) index = i;
			}
			if (index < 0) quit("fixture: missing spell");
			fixture_add(TV_MAGIC_BOOK, "[Attacks and Knowledge]", 1);
			if (!(player->spell_flags[index] & PY_SPELL_LEARNED)) spell_learn(index);
			if (player->csp < spell_by_index(player, index)->smana)
				player->csp = player->msp;
		} else if (prefix(mode, "priest-")) {
			if (player->class->cidx != 3) quit("fixture: expected Priest");
			fixture_room();
			struct object *dagger = fixture_add(TV_SWORD, "Dagger", 1);
			dagger->to_h = 2;
			dagger->el_info[ELEM_NEXUS].res_level = 1;
			if (streq(mode, "priest-scroll")) fixture_add(TV_SCROLL, "Identify Rune", 3);
			update_player_object_knowledge(player);
			if (object_runes_known(dagger)) quit("fixture: spare must remain unknown");
			player->word_recall = 65;
			option_set("auto_more", true);
		} else quit("fixture: invalid mode");
		if (pack_is_overfull()) quit("fixture: overfull pack");
		if (!out || !savefile_save(out)) quit("fixture: save failed");
	}
	fixture_inventory(stderr);
	exit(0);
}
