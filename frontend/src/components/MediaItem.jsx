import React from 'react'
import { Img } from 'react-image'

const MediaItem = ({
    data,
    onClick
}) => {

    const handleClick = () => {
        onClick(data.id)
    }
    
  return (
    <div onClick={handleClick} className='flex items-center gap-x-3 cursor-pointer hover:bg-neutral-800/50 w-full p-2 rounded-md'>
        <div className='relative rounded-md max-h-[48px] max-w-[48px] overflow-hidden'>
            <Img src={data.cover_art} alt='Media Item' className='object-cover' />
        </div>
        <div className='flex flex-col gap-y-1 overflow-hidden'>
            <p className='text-white truncate'>
                {data.title}
            </p>
            <p className='text-neutral-400 text-sm truncate'>
                {data.artist}
            </p>
        </div>
    </div>
  )
}

export default MediaItem