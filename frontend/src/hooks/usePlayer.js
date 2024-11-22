const { create } = require("zustand");

const usePlayer = create((set) => ({
    ids: [],
    activeId: undefined,
    setId: (id) => set({activeId: id}),
    setIds: (ids) => set({ids: ids}),
    reset: () => set({ids: [], activeId: undefined})
}))

export default usePlayer