def dump_tree(window):
    print("\n========== UI ELEMENT TREE ==========")
    try:
        window.print_control_identifiers()
    except Exception as e:
        print(f"ไม่สามารถ dump tree ได้: {e}")
    print("=====================================\n")
