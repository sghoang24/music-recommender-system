import React from 'react'
import SongItem from '../../../components/SongItem'
import useOnPlay from 'hooks/useOnPlay'
import Spinner from '../../../components/Spinner'

const PageContent = ({songs, isLoading}) => {
    const onPlay = useOnPlay(songs)
    if (songs.length === 0) {
        return (
            <div className='mt4
             text-neutral-400'>
                No songs available.
            </div>
        )
    }

  return (
    (!songs) ? (
        <div className='flex justify-center items-center'>
            <Spinner/>
        </div>
    ) : (
        <div className='grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-8 gap-4 mt-4'>
            {songs.map((item) => (
                <SongItem data={item} key={item.id} onClick={(id) => onPlay(id)}/>
            ))}
        </div>
    )
  )
}

export default PageContent