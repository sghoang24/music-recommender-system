import usePlayer from 'hooks/usePlayer'
import React, { useEffect, useState } from 'react'
import useGetSongById from 'hooks/useGetSongById'
import PlayerContent from './PlayerContent'

const Player = () => {
    const player = usePlayer()
    const {song} = useGetSongById(player.activeId)

    const songUrl = song ? song.mp3_url : ""

    if (!song || !songUrl || !player.activeId) {
        return null
    }
    
  return (
    <div className='fixed bottom-0 bg-black w-full py-2 h-[80px] px-4'>
        <PlayerContent key={songUrl} song={song} songUrl={songUrl}/>
    </div>
  )
}

export default Player