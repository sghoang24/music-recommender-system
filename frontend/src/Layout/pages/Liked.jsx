import React, { useContext, useEffect, useState } from 'react'
import Header from '../../components/Header'
import { Img } from 'react-image'
import LikedContent from './components/LikedContent'
import { UserContext } from 'context/UserContext'
import api from 'api'
import { twMerge } from 'tailwind-merge'
import usePlayer from 'hooks/usePlayer'

const Liked = () => {
    const [userData, setUserData] = useContext(UserContext)
    const player = usePlayer()
    const [songs, setSongs] = useState([])
    useEffect(() => {
        // fetch liked songs
        const fetchSongs = async () => {
            try {
                const response = await api.get(`/get_liked_tracks/${userData.user.id}`)
                if (response.status === 200) {
                    setSongs(response.data)
                }
            } catch (error) {
                console.log(error)
            }
        }
        if (userData.user?.id) {
            fetchSongs()
        }
    }, [])
  return (
    <div className={twMerge(`bg-neutral-900 rounded-lg h-[97.6vh] w-[99.8%] overflow-hidden overflow-y-auto`, player.activeId && "h-[calc(97.6vh-72px)]")}
    >
        <Header>
            <div className='mt-20'>
                <div className='flex flex-col md:flex-row items-center gap-x-5'>
                    <div className='relative h-32 w-32 lg:h-44 lg:w-44'>
                        <Img fill="true" alt='Playlist' className='object-cover' src="/images/liked.png"/>
                    </div>
                    <div className='flex flex-col gap-y-2 mt-4 md:mt-0'>
                        <p className='hidden md:block font-semibold text-sm'>
                            Playlist
                        </p>
                        <h1 className='text-white text-4xl sm:text-5xl lg:text-7xl font-bold'>
                            Liked Songs
                        </h1>
                    </div>
                </div>
            </div>
        </Header>
        <LikedContent songs={songs}/>
    </div>
  )
}

export default Liked