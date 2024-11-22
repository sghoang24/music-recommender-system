import { useState, useEffect, useMemo } from "react"
import api from "api"

const useGetRecommendSongs = (id) => {
    const [songs, setSongs] = useState([]) 
    const [isLoading, setIsLoading] = useState(false)

    useEffect(() => {
        if (!id) {
            return
        }
        setIsLoading(true)

        const fetchSongs = async () => {
            try {
                const response = await api.get(`/get_recommendation/${id}`)
                if (response.status === 200) {
                    console.log(response.data);
                    setSongs(response.data)
                    setIsLoading(false)
                }
            } catch (error) {
                console.log(error)
                setIsLoading(false)
            }
        }
        fetchSongs()
    }, [id])

    return useMemo(() => ({
        isLoading, 
        songs
    }), [isLoading, songs])
}

export default useGetRecommendSongs