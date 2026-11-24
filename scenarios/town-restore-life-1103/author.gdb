set pagination off
set disable-randomization off
set confirm off
set debuginfod enabled off
break main-borgh.c:895
run
python
import gdb
import json
import os

def value(expr):
    return gdb.parse_and_eval(expr)

def save(name):
    path = os.path.join(os.environ["FIXTURE_SAVE_DIR"], name + ".save")
    assert int(value(f"(int)savefile_save({json.dumps(path)})"))

assert int(value("player->depth")) == 0
assert int(value("player->max_depth")) >= 12
gdb.execute("set player->exp = player->max_exp")
gdb.execute("set player->lev = player->max_lev")
gdb.execute("set player->au = 999")
# Provide headroom and eliminate competing Home and shop wares for this
# native checkout check. All arms use the same equipment and retained gear.
gdb.set_convenience_variable("gone", value("(unsigned char *)mem_zalloc(1)"))
gdb.set_convenience_variable("walk", value("player->gear"))
bulk = {int(value(tval)) for tval in ("TV_SHOT", "TV_MUSHROOM", "TV_ROD", "TV_WAND", "TV_STAFF")}
while int(value("$walk")):
    gdb.execute("set $next = $walk->next")
    if int(value("$walk->tval")) in bulk and not int(value("(int)object_is_equipped(player->body, $walk)")):
        value("(struct object *)gear_object_for_use(player, $walk, $walk->number, 0, $gone)")
    gdb.execute("set $walk = $next")
value("(void)update_stuff(player)")
for i in range(int(value("z_info->store_max"))):
    gdb.set_convenience_variable("shop", value(f"&stores[{i}]"))
    value("(void)object_pile_free(0, 0, $shop->stock_k)")
    value("(void)object_pile_free(0, 0, $shop->stock)")
    gdb.execute("set $shop->stock_k = 0")
    gdb.execute("set $shop->stock = 0")
    gdb.execute("set $shop->stock_num = 0")

def stock_potion(name, feature, price):
    kind = value(f'(struct object_kind *)lookup_kind(TV_POTION, lookup_sval(TV_POTION, "{name}"))')
    gdb.set_convenience_variable("kind", kind)
    gdb.set_convenience_variable("obj", value("(struct object *)object_new()"))
    value("(void)object_prep($obj, $kind, 12, AVERAGE)")
    gdb.execute("set $obj->known = (struct object *)object_new()")
    value("(void)object_flavor_aware(player, $obj)")
    value("(void)object_set_base_known(player, $obj)")
    value("(void)player_know_object(player, $obj)")
    gdb.set_convenience_variable("shop", value(f"&stores[f_info[{feature}].shopnum - 1]"))
    if feature == "FEAT_STORE_BLACK":
        assert int(value("(int)black_market_ok($obj)"))
    assert int(value("(struct object *)store_carry($shop, $obj, 0)"))
    assert int(value("$shop->stock_num")) == 1
    assert int(value("(int)price_item($shop, $shop->stock, 0, 1)")) == price

stock_potion("Restore Life Levels", "FEAT_STORE_ALCHEMY", 400)
print("CL / DL / maximum DL / gold / price:", *(int(value(x)) for x in ("player->lev", "player->depth", "player->max_depth", "player->au", "(int)price_item($shop, $shop->stock, 0, 1)")))
save("healthy-999")
gdb.execute("set player->au = 1000")
save("healthy-1000")
gdb.execute("set player->au = 999")
gdb.execute("set player->exp = player->max_exp - 100")
save("drained-999")
gdb.execute("set player->exp = player->max_exp")
value("(void)object_pile_free(0, 0, $shop->stock_k)")
value("(void)object_pile_free(0, 0, $shop->stock)")
gdb.execute("set $shop->stock_k = 0")
gdb.execute("set $shop->stock = 0")
gdb.execute("set $shop->stock_num = 0")
stock_potion("Restore Life Levels", "FEAT_STORE_BLACK", 1200)
gdb.execute("set player->au = 2999")
save("market-2999")
gdb.execute("set player->au = 3000")
save("market-3000")
end
kill
