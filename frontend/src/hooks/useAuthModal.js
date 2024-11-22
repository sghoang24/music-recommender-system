import { create } from 'zustand' 

const useAuthModal = create((set) => ({
    isOpen : false,
    method : "",
    onOpenLogin : () => set({ isOpen : true, method : "login" }),
    onOpenSignup : () => set({ isOpen : true, method : "signup" }),
    onOpenSurvey : () => set({isOpen : true, method : "survey"}),
    onClose : () => set({ isOpen : false, method: ""})
}))

export default useAuthModal