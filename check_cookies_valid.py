def validate_netscape_cookie_file(filename):
    valid = True
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # Skip comments and empty lines

        parts = line.split("\t")
        if len(parts) != 7:
            print(f"❌ Invalid line {idx}: Expected 7 fields, got {len(parts)}")
            print(f"    → {line}")
            valid = False

    if valid:
        print("✅ The cookies file is valid Netscape format.")
    else:
        print("⚠️ The cookies file contains errors.")

# Example usage:
validate_netscape_cookie_file("cookies.txt")