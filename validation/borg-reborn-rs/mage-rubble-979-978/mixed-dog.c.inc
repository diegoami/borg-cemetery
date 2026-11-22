static void prepare_borg_start(void)
{
    if (opt_load) {
        for (int y = 54; y <= 55; y++)
            for (int x = 126; x < 133; x++)
                square_set_feat(cave, loc(x, y), FEAT_FLOOR);
        struct monster_group_info info = {0};
        if (!place_new_monster(cave, loc(126, 54), lookup_monster("wild dog"),
                               false, false, info, ORIGIN_DROP_WIZARD))
            quit("could not place clear dog");
        update_view(cave, player);
    }
