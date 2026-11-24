#include "obj-desc.h"
#include "player-spell.h"
#include "player-attack.h"

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

static void fixture_remove_gear(void)
{
	struct object *obj = player->gear;
	while (obj) {
		struct object *next = obj->next;
		if (!object_is_equipped(player->body, obj)) {
			bool none_left;
			struct object *removed = gear_object_for_use(player, obj, obj->number, false, &none_left);
			if (removed->known) object_delete(NULL, NULL, &removed->known);
			object_delete(NULL, NULL, &removed);
		}
		obj = next;
	}
	update_stuff(player);
}

static void fixture_encounter(const char *mode)
{
	const bool priest = player->class->cidx == 3;
	option_set("auto_more", true);
	const char *offset = getenv("CASE_TARGET_DISTANCE");
	const int distance = offset ? atoi(offset) : 4;
	const struct loc target = loc_sum(player->grid, loc(distance, 0));
	const char *target_name = getenv("CASE_TARGET");
	struct monster_group_info group = { 0, 0 };
	fixture_room();
	fixture_remove_gear();
	struct object *worn = priest
		? fixture_add(TV_HAFTED, streq(mode, "throw-spear") ? "Morning Star" : "Mace", 1)
		: fixture_add(TV_SWORD, "Dagger", 1);
	struct object *spare = fixture_add(streq(mode, "throw-spear") ? TV_POLEARM : TV_SWORD,
		streq(mode, "throw-spear") ? "Spear" : "Dagger", 1);
	worn->to_h = 5;
	worn->to_d = 5;
	update_player_object_knowledge(player);
	while (!object_runes_known(worn)) object_learn_unknown_rune(player, worn);
	while (!object_runes_known(spare)) object_learn_unknown_rune(player, spare);
	if (streq(mode, "throw-unknown")) {
		spare->el_info[ELEM_NEXUS].res_level = 1;
		update_player_object_knowledge(player);
		if (object_runes_known(spare)) quit("fixture: spare must remain unknown");
	}
	if (streq(mode, "throw-upgrade")) {
		spare->to_d = 8;
		update_player_object_knowledge(player);
	}
	inven_wield(worn, slot_by_name(player, "weapon"));
	struct object *previous = player->gear;
	while (previous) {
		struct object *next = previous->next;
		if (previous != spare && !object_is_equipped(player->body, previous)) {
			bool none_left;
			gear_object_for_use(player, previous, previous->number, false, &none_left);
		}
		previous = next;
	}
	if (streq(mode, "throw-device")) {
		struct object *device = fixture_add(TV_WAND, "Acid Bolts", 1);
		device->pval = 12;
		device->known->pval = 12;
	}
	if (streq(mode, "throw-spell")) {
		fixture_add(TV_MAGIC_BOOK, "[First Spells]", 1);
		player->csp = player->msp;
	} else {
		player->csp = 0;
	}
	if (streq(mode, "throw-launcher")) {
		struct object *launcher = fixture_add(TV_BOW, "Sling", 1);
		launcher->to_h = launcher->to_d = 10;
		update_player_object_knowledge(player);
		while (!object_runes_known(launcher)) object_learn_unknown_rune(player, launcher);
		inven_wield(launcher, slot_by_name(player, "shooting"));
		struct object *shot = fixture_add(TV_SHOT, "Iron Shot", 12);
		shot->to_h = shot->to_d = 8;
		update_player_object_knowledge(player);
	}
	player->word_recall = 0;
	player->timed[TMD_FOOD] = 7500;
	player->csp_frac = 0;
	player->upkeep->energy_use = 0;
	option_set("show_damage", true);
	option_set("auto_more", true);
	if (!place_new_monster(cave, target, lookup_monster(target_name ? target_name : "kobold"), false, false, group, ORIGIN_DROP_WIZARD))
		quit("fixture: cannot place monster");
	update_stuff(player);
	player->chp = player->mhp;
	fprintf(stderr, "combat\t%d\t%d\t%d\t%d\n", priest, distance,
		adj_str_blow[player->state.stat_ind[STAT_STR]], player->state.skills[SKILL_TO_HIT_THROW]);
}

static void fixture_attack_probabilities(void)
{
	const char *offset = getenv("CASE_TARGET_DISTANCE");
	int distance = offset ? atoi(offset) : 4;
	int ac = lookup_monster("kobold")->ac;
	struct object *worn = equipped_item_by_slot_name(player, "weapon");
	struct object *bow = equipped_item_by_slot_name(player, "shooting");
	random_chance chance;
	hit_chance(&chance, chance_of_melee_hit_base(player, worn), ac);
	fprintf(stderr, "native-melee\t%d/%d\n", chance.numerator, chance.denominator);
	fprintf(stderr, "native-melee-to-dam\t%d\n", player->state.to_d);
	for (struct object *item = player->gear; item; item = item->next) {
		if (item->tval == TV_SHOT && bow) {
			int to_h = player->state.to_h + object_to_hit(item) + object_to_hit(bow);
			int skill = player->state.skills[SKILL_TO_HIT_BOW];
			hit_chance(&chance, skill + to_h * BTH_PLUS_ADJ - distance, ac);
			fprintf(stderr, "native-shot\t%d/%d\n", chance.numerator, chance.denominator);
		} else if (item->tval == TV_WAND) {
			fprintf(stderr, "native-device-success\t%d/1000\n", 1000 - get_use_device_chance(item));
		}
	}
	for (int i = 0; i < player->class->magic.total_spells; ++i) {
		const struct class_spell *spell = spell_by_index(player, i);
		if (streq(spell->name, "Electric Arc"))
			fprintf(stderr, "native-electric-arc-success\t%d/100\n", 100 - spell_chance(i));
	}
}
static void fixture_prepare(void)
{
	const char *mode = getenv("CASE_FIXTURE_MODE");
	const char *out = getenv("CASE_FIXTURE_SAVE");
	if (!mode) return;
	if (streq(mode, "inspect-combat")) fixture_attack_probabilities();
	if (!prefix(mode, "inspect")) {
		if (prefix(mode, "throw-")) {
			fixture_encounter(mode);
		} else quit("fixture: invalid mode");
		if (pack_is_overfull()) quit("fixture: overfull pack");
		if (!out || !savefile_save(out)) quit("fixture: save failed");
	}
	fixture_inventory(stderr);
	exit(0);
}
