import { useState, useEffect, useMemo, useContext } from "react"
import api from "api"
import { UserContext } from "context/UserContext"

const useGetHomeSongs = () => {
    const [songs, setSongs] = useState([]) 
    const [isLoading, setIsLoading] = useState(false)
    const [userData,] = useContext(UserContext)

    useEffect(() => {
    
        setIsLoading(true)
        const fetchSongs = async () => {
            try {
                if (userData.token) {
                    const response = await api.get(`/get_tracks_for_user/${userData.user.id}`)

                    if (response.status === 200) {
                        setSongs(response.data)
                        setIsLoading(false)
                    }
                }
                else {
                    const response = await api.get('/get_10_tracks')

                    if (response.status === 200) {
                        setSongs(response.data)
                        setIsLoading(false)
                    }
                }
            } catch (error) {
                console.log(error)
                setIsLoading(false)
            }
        }
        fetchSongs()
    }, [userData.token, userData.preferences])

    return useMemo(() => ({
        isLoading, 
        songs
    }), [isLoading, songs])
}

export default useGetHomeSongs