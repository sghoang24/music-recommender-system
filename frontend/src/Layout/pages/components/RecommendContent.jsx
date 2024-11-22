import { useState, useEffect } from 'react'
import ListRowItem from '../../../components/ListRowItem'
import usePlayer from 'hooks/usePlayer'
import useOnPlay from 'hooks/useOnPlay'


const RecommendContent = ({
    songs
}) => {
    // const navigate = useNavigate()
    const player = usePlayer() 
    const onPlay = useOnPlay(songs)
    
    useEffect(() => {
        player.setIds(songs.map(song => song.id))
    }, [songs])

  return (
    <div className='flex flex-col gap-y-2 w-full p-6'>
        {songs.map((song) => (
            <ListRowItem song={song} onClick={(id) => onPlay(id)}/>
        ))}
    </div>
  )
}

export default RecommendContent