import React, { useEffect, useState } from 'react'
import MediaItem from './MediaItem'
import LikeButton from './LikeButton'
import Slider from './Slider'
import {BsPauseFill, BsPlayFill} from 'react-icons/bs'
import { AiFillStepBackward, AiFillStepForward } from 'react-icons/ai'
import {HiSpeakerWave, HiSpeakerXMark} from 'react-icons/hi2'
import { MdOutlineQueueMusic } from "react-icons/md"
import usePlayer from 'hooks/usePlayer'
import useSound from 'use-sound'
import { useNavigate } from 'react-router-dom'

const PlayerContent = ({
    song, 
    songUrl
}) => {
    const player = usePlayer()
    const navigate = useNavigate()
    const [volume, setVolume] = useState(0.5)
    const [isPlaying, setIsPlaying] = useState(false)
    const Icon = isPlaying ? BsPauseFill : BsPlayFill
    const VolumeIcon = volume===0 ? HiSpeakerXMark : HiSpeakerWave

    const onPlayNext = () => {
        if (player.ids.length === 0 ) {
            return
        }
        const currentIndex = player.ids.findIndex((id) => id === player.activeId)
        const nextSong = player.ids[currentIndex + 1]

        if (!nextSong) {
            return player.setId(player.ids[0])
        }
        player.setId(nextSong)
    }

    const onPlayPrevious = () => {
        if (player.ids.length === 0 ) {
            return
        }
        const currentIndex = player.ids.findIndex((id) => id === player.activeId)
        const previousSong = player.ids[currentIndex - 1]

        if (!previousSong) {
            return player.setId(player.ids[player.ids.length - 1])
        }
        player.setId(previousSong)
    }

    const [play, {pause, sound}] = useSound(
        songUrl,
        {
            volume: volume,
            onplay: () => setIsPlaying(true),
            onend: () => {
                setIsPlaying(false)
                onPlayNext() 
            },
            onpause: () => setIsPlaying(false),
            format: ['mp3']
        }
    )

    useEffect(() => {
        sound?.play() 

        return () => {
            sound?.unload()
        }
    }, [sound])

    const handlePlay = () => {
        if (!isPlaying) {
            play()
        } else {
            pause()
        }
    }

    const toggleMute = () => {
        if (volume === 0) { 
            setVolume(0.5)
        } else {
            setVolume(0)
        }
    }

  return (
    <div className='grid grid-cols-2 md:grid-cols-3 h-full'>
        <div className='flex w-full justify-start'>
            <div className='flex items-center gap-x-4'>
                <MediaItem data={song} onClick={() => {}}/>
                <LikeButton songId={song.id}/>
            </div>
        </div>

        {/* mobile view */}
        <div className='flex md:hidden col-auto w-full justify-end items-center'>
            <MdOutlineQueueMusic size={30} className='cursor-pointer text-white mr-3' title='Recommend songs' onClick={() => navigate(`/recommend/${song.id}`)}/>
            <div onClick={handlePlay} className='h-10 w-10 flex items-center justify-center rounded-full bg-white p-1 cursor-pointer'>
                <Icon size={30} className='text-black'/>
            </div>
        </div>

        {/* desktop view */}
        <div className='hidden h-full md:flex justify-center items-center w-full max-w-[722px] gap-x-6'>
            <AiFillStepBackward size={30} className='text-neutral-400 cursor-pointer hover:text-white transition' onClick={onPlayPrevious}/>
            <div className='flex items-center justify-center h-10 w-10 rounded-full bg-white p-1 cursor-pointer' onClick={handlePlay}>
                <Icon size={30} className='text-black'/>
            </div>
            <AiFillStepForward size={30} onClick={onPlayNext} className='text-neutral-400 cursor-pointer hover:text-white transition'/>
        </div>


        <div className='hidden md:flex w-full justify-end pr-2'>
            <div className='flex items-center gap-x-2 w-[180px]'>
                <MdOutlineQueueMusic size={36} className='cursor-pointer text-white mr-3' title='Recommend songs' onClick={() => navigate(`/recommend/${song.id}`)}/>
                <VolumeIcon onClick={toggleMute} className='cursor-pointer' size={34}/>
                <Slider value={volume} onChange={(value) => setVolume(value)}/>
            </div>
        </div>
    </div>
  )
}

export default PlayerContent