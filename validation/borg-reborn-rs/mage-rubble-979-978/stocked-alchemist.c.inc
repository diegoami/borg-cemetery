#include "store.h"
static void prepare_borg_start(void)
{
    if (opt_load) {
        bool auto_more = OPT(player, auto_more);
        dungeon_change_level(player, 0);
        option_set("auto_more", true);
        borgh_generate_start();
        event_signal(EVENT_MESSAGE_FLUSH);
        player->stat_cur[STAT_STR] = player->stat_max[STAT_STR] = 118;
        player->upkeep->update |= PU_BONUS;
        if (getenv("BORGH_TRIAL_HEALTHY")) player->exp = player->max_exp;
        while (player->upkeep->total_weight > 1200) {
            struct object *heavy = NULL;
            for (struct object *obj = player->gear; obj; obj = obj->next) {
                if (!object_is_equipped(player->body, obj) && (!heavy || obj->weight * obj->number > heavy->weight * heavy->number)) heavy = obj;
            }
            if (!heavy) break;
            bool none_left;
            struct object *removed = gear_object_for_use(player, heavy, heavy->number, false, &none_left);
            object_delete(NULL, NULL, &removed->known);
            object_delete(NULL, NULL, &removed);
        }
        int sval = lookup_sval(TV_POTION, "Restore Life Levels");
        struct object_kind *kind = lookup_kind(TV_POTION, sval);
        struct object *potion = object_new();
        object_prep(potion, kind, 0, MINIMISE);
        potion->number = 1;
        potion->known = object_new();
        object_set_base_known(player, potion);
        object_flavor_aware(player, potion);
        potion->known->effect = potion->effect;
        potion->known->notice |= OBJ_NOTICE_ASSESSED;
        if (!store_carry(&stores[4], potion, false))
            quit("controlled Alchemist offer did not fit");
        event_signal(EVENT_MESSAGE_FLUSH);
        option_set("auto_more", auto_more);
    }
