from handbook import is_unlocked

def test_empty():
    assert is_unlocked([], "COMP1511") == True
    assert is_unlocked([], "COMP9301") == False
    assert is_unlocked([], 'COMP9491') == False
    assert is_unlocked([], 'COMP3901') == False
    assert is_unlocked([], 'COMP4161') == False

def test_single():
    assert is_unlocked(["MATH1081"], "COMP3153") == True
    assert is_unlocked(["ELEC2141"], "COMP3211") == True
    assert is_unlocked(["COMP1511", "COMP1521", "COMP1531"], "COMP3153") == False
    assert is_unlocked(["MATH1081"], "COMP2111") == False
    assert is_unlocked(["MATH1081", "COMP1511"], "COMP2111") == True

def test_uoc():
    assert is_unlocked(["COMP1511", "COMP1521", "COMP1531", "COMP2521"], "COMP4161") == True
    assert is_unlocked(["COMP1511", "COMP1521"], "COMP4161") == False
    assert is_unlocked(["COMP3901"], "COMP3902") == False
    assert is_unlocked(["COMP3901", "COMP6441", "COMP6443"], "COMP3902") == False
    assert is_unlocked(["COMP3901", "COMP3441", "COMP3443"], "COMP3902") == True
    assert is_unlocked(["COMP1234", "COMP5634", "COMP4834"], "COMP9491") == False
    assert is_unlocked(["COMP3821"], "COMP4128") == True
    assert is_unlocked(["COMP3121", "COMP3901", "COMP3141"], "COMP4128") == True
    assert is_unlocked(["COMP3121", "COMP2511", "COMP1511"], "COMP4128") == False
