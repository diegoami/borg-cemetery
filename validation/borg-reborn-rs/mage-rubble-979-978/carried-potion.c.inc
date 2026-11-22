static void prepare_borg_start(void)
{
    if (opt_load) {
        wipe_mon_list(cave, player);
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
        if (!inven_carry_okay(potion)) quit("trial requires a free pack slot");
        inven_carry(player, potion, true, false);
        fprintf(stderr, "Controlled potion trial: XP %ld/%ld\n", (long)player->exp, (long)player->max_exp);
        event_signal(EVENT_MESSAGE_FLUSH);
    }
