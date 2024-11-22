import React from 'react'
import { useNavigate } from 'react-router-dom'
import {Img} from 'react-image'
import {FaPlay} from 'react-icons/fa'

const ListItem = ({
    image, 
    name, 
    href
}) => {
    const navigate = useNavigate()
    const onclick = () => {
        // Add authenciation before push
        navigate(href)
    }
  return (
    <button className='relative group flex items-center rounded-md overflow-hidden gap-x-4 bg-neutral-100/10 hover:bg-neutral-100/20 transition pr-4' onClick={onclick}>
        <div className='relative min-h-[64px] min-w-[64px]'>
            <Img className="object-cover h-16" src={image} alt="Image"/>
        </div>
        <p className='font-medium truncate py-5'>
            {name}
        </p>
        <div className='absolute transition opacity-0 rounded-full flex items-center justify-center bg-green-500 p-4 drop-shadow-md right-5 group-hover:opacity-100 hover:scale-110'>
            <FaPlay className='text-black'/>
        </div>
    </button>
  )
}

export default ListItem