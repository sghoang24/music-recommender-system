import React, {useContext, useEffect} from 'react'
import { useNavigate } from 'react-router-dom'
import { UserContext } from 'context/UserContext'
import MediaItem from '../../../components/MediaItem'
import LikeButton from '../../../components/LikeButton'
import useOnPlay from 'hooks/useOnPlay'

const LikedContent = ({
    songs
}) => {
    const navigate = useNavigate() 
    const onPlay = useOnPlay(songs)
    const [userData, ] = useContext(UserContext)
    useEffect(() => {
        if (!userData.user) {
            navigate('/') 
        }
    }, [userData.user, navigate])
    if (songs.length === 0) {
        return (
            <div className='flex flex-col gap-y-2 w-full px-6 text-neutral-400'>
                No liked songs.
            </div>
        )
    }
  return (
    <div className='flex flex-col gap-y-2 w-full p-6'>
        {songs.map((song) => (
            <div key={song.id} className='flex items-center gap-x-4 w-full'>
                <div className='flex-1'>
                    <MediaItem onClick={(id) => onPlay(id)} data={song}/>
                </div>
                <LikeButton songId={song.id}/>
            </div>
        ))}
    </div>
  )
}

export default LikedContent