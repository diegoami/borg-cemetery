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

#include "store.h"

static void fixture_prepare(void)
{
	const char *out = getenv("CASE_FIXTURE_SAVE");
	const char *gold = getenv("CASE_GOLD");
	if (!out || !gold) return;
	if (player->class->cidx != 0 || player->depth != 0)
		quit("fixture: expected warrior in town");
	option_set("auto_more", true);
	player->max_depth = player->recall_depth = 7;
	while (player->lev < 22) player_exp_gain(player, 50);
	player->au = atoi(gold);
	struct object *sling = fixture_add(TV_BOW, "Sling", 1);
	sling->to_h = 15;
	sling->to_d = 6;
	update_player_object_knowledge(player);
	while (!object_runes_known(sling)) object_learn_unknown_rune(player, sling);
	inven_wield(sling, slot_by_name(player, "shooting"));
	fixture_add(TV_SCROLL, "Phase Door", 12);
	fixture_add(TV_POTION, "Cure Serious Wounds", 8);
	player->upkeep->energy_use = 0;
	player->chp = player->mhp;
	struct store *general = &stores[f_info[FEAT_STORE_GENERAL].shopnum - 1];
	bool offer = false;
	for (struct object *item = general->stock; item; item = item->next) {
		if (item->tval == TV_SHOT) {
			int price = price_item(general, item, false, 1);
			fprintf(stderr, "offer\t%d\t%d\t%s\n", item->number, price, item->kind->name);
			offer = true;
		}
	}
	if (!offer) quit("fixture: no ordinary shots available");
	fixture_inventory(stderr);
	if (!savefile_save(out)) quit("fixture: save failed");
	exit(0);
}
