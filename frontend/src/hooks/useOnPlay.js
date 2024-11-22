import { useContext } from "react"
import useAuthModal from "./useAuthModal"
import usePlayer from "./usePlayer"
import { UserContext } from "context/UserContext"

const useOnPlay = (songs) => {
    const player = usePlayer() 
    const authModal = useAuthModal() 
    const [userData, ] = useContext(UserContext) 

    const onPlay = (id) => {
        if (!userData.user) {
            return authModal.onOpenLogin() 
        }

        player.setId(id) 
        player.setIds(songs.map(song => song.id))
    }

    return onPlay
}

export default useOnPlay