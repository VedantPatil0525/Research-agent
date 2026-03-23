# ─────────────────────────────────────────────
# MEMORY STORAGE
# ─────────────────────────────────────────────

memory_store = []


# ➕ Add data to memory (with validation)
def add_to_memory(data):
    if not isinstance(data, dict):
        return

    # Avoid duplicates (same source + task)
    for item in memory_store:
        if item.get("source") == data.get("source") and item.get("task") == data.get("task"):
            return

    memory_store.append(data)


# 📥 Get all memory
def get_memory():
    return memory_store


# 🧹 Clear memory (VERY IMPORTANT for UI runs)
def clear_memory():
    global memory_store
    memory_store = []


# 📊 Get memory count (optional utility)
def memory_size():
    return len(memory_store)