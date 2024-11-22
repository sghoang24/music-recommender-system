import React, { useContext, useEffect, useState } from 'react'
import Header from '../../components/Header'
import ListItem from '../../components/ListItem'
import PageContent from './components/HomeContent'
import ModalProvider from 'context/ModalProvider'
import { twMerge } from 'tailwind-merge'
import usePlayer from 'hooks/usePlayer'
import { UserContext } from 'context/UserContext'
import useGetHomeSongs from 'hooks/useGetHomeSongs'

const Home = () => {

  // const [songs, setSongs] = useState([])
  const {songs, isLoading} = useGetHomeSongs()
  const player = usePlayer()
  const [userData, ] = useContext(UserContext) 
  
  // useEffect(() => {
  //   const fetchSongs = async () => {
  //     try {
  //       if (userData.token) {
  //         const response = await api.get(`/get_recommendation_by_likes/${userData.user.id}`)
  //         if (response.status === 200) {
  //           setSongs(response.data)
  //         }
  //         // setFetched(true)
  //       } 
  //       else if (!userData.token) {
  //         const response = await api.get('/get_10_tracks')
  //         if (response.status === 200) {
  //           console.log(response.data);
  //           setSongs(response.data)
  //           // setFetched(true)
  //         }
  //       }
  //     } catch (error) {
  //       console.log(error)
  //     }
  //   }
  //   fetchSongs()
  // }, [userData])
  
  
  return (
    <div>
      <ModalProvider />
      <div className={twMerge(`bg-neutral-900 rounded-lg h-[97.6vh] w-[99.8%] overflow-hidden overflow-y-auto`, player.activeId && "h-[calc(97.6vh-72px)]")}
      >
        <Header>
          <div className='mb-2'>
            <h1 className='text-white text-3xl font-semibold'>
              Welcome back
            </h1>
            <div className='grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-3 mt-4'>
              <ListItem image="/images/liked.png" name="Liked Songs" href="/liked"/>
            </div>
          </div>
        </Header>
        <div className='mt-2 mb-7 px-6'>
          <div className='flex justify-between items-center'>
            {(!userData.token) ? (
              <h1 className='text-white text-2xl font-semibold'>
                Songs for you
              </h1>
            ) : (
              <h1 className='text-white text-2xl font-semibold'>
                Recommended for you
              </h1>
            )}
          </div>
          <div>
            <PageContent songs={songs} isLoading={isLoading}/>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home