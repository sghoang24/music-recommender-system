import ModalProvider from 'context/ModalProvider'
import usePlayer from 'hooks/usePlayer'
import React, { useContext, useEffect, useState } from 'react'
import { twMerge } from 'tailwind-merge'
import Header from '../../components/Header'
import { useParams } from 'react-router-dom'
import { Img } from 'react-image'
import RecommendContent from './components/RecommendContent'
import { UserContext } from 'context/UserContext'
import api from 'api'
import useGetRecommendSongs from 'hooks/useGetRecommendSongs'

const Recommend = () => {
    const player = usePlayer() 
    const { songId } = useParams()
    const {songs} = useGetRecommendSongs(songId)

  return (
    <div>
      <ModalProvider/>
      <div className={twMerge(`bg-neutral-900 rounded-lg h-[97.6vh] w-[99.8%] overflow-hidden overflow-y-auto`, player.activeId && "h-[calc(97.6vh-72px)]")}
      >
        <Header>
          <div className='mt-20'>
            <div className='flex flex-col md:flex-row items-center gap-x-5'>
              <div className='relative h-32 w-32 lg:h-44 lg:w-44'>
                <Img fill="true" alt='Playlist' className='object-cover' src="/images/liked.png"/>
              </div>
              <div className='flex flex-col gap-y-2 mt-4 md:mt-0'>
                <h1 className='text-white text-4xl sm:text-5xl lg:text-7xl font-bold'>
                  Recommended songs
                </h1>
                <p className='hidden md:block font-semibold text-sm'>
                  We think you might like
                </p>
              </div>
            </div>
          </div>
        </Header>
        <RecommendContent songs={songs}/>
      </div>
    </div>
  )
}

export default Recommend