import { useState, useEffect, useMemo } from 'react'
import api from 'api'

const useGetSongById = (id) => {
    const [isLoading, setIsLoading] = useState(false) 
    const [song, setSong] = useState(undefined) 
    
    useEffect(() => {
        if (!id) {
            return
        }
        setIsLoading(true)

        const fetchSong = async () => {
            try {
                const response = await api.get(`/get_track_by_id/${id}`)
                if (response.status === 200) {
                    setSong(response.data)
                    setIsLoading(false)
                }
            } catch (error) {
                console.log(error)
                setIsLoading(false)
            }
        }

        fetchSong()
    }, [id])

    return useMemo(() => ({
        isLoading,
        song
    }), [isLoading, song])
}

export default useGetSongById