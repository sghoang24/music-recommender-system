import React, { useEffect, useState } from 'react'
import Header from '../../components/Header'
import Filter from '../../components/Filter'
import SearchInput from '../../components/SearchInput'
import SearchContent from './components/SearchContent'
import qs from 'query-string'
import { useLocation } from 'react-router-dom'
import api from 'api'
import ModalProvider from 'context/ModalProvider'
import usePlayer from 'hooks/usePlayer'
import { twMerge } from 'tailwind-merge'
import { select } from '@material-tailwind/react'

const Search = () => {
  // TODO : write function to search songs by title
  const location = useLocation() 
  const player = usePlayer()
  const [searchQuery, setSearchQuery] = useState("")
  const [songs, setSongs] = useState([])  
  const [selectedGenres, setSelectedGenres] = useState(['All'])

  useEffect(() => {
    const query = qs.parse(location.search)
    setSearchQuery(query.title || '') 
  }, [location.search])

  useEffect(() => {
    const fetchSongs = async () => {
      try {
        if (searchQuery !== "" && selectedGenres.length > 0) {
          const genreParams = selectedGenres.join(",") 
          // const response = await api.get(`/search_tracks/${searchQuery}`)
          const response = await api.get(`/search_tracks`, {
            params: {
              search_query : searchQuery,
              genres : (selectedGenres.length === 1 && selectedGenres[0] === 'All') ? 'All' : genreParams
            }
          })
          
          if (response.status === 200) {
            // console.log(response.data)
            setSongs(response.data)
          }
        }
        else {
          setSongs([])
        }
      } catch (error) {
        console.log(error)
        setSongs([])
      }
    }
    fetchSongs()
  }, [searchQuery, selectedGenres])
  return (
    <div className={twMerge(`bg-neutral-900 rounded-lg h-[97.6vh] w-[99.8%] overflow-hidden overflow-y-auto`, player.activeId && "h-[calc(97.6vh-72px)]")}
    >
      <ModalProvider/>
      <Header className="from-bg-neutral-900">
        <div className='mb-2 flex flex-col gap-y-6'>
          <h1 className='text-white text-3xl font-semibold'>
            Search
          </h1>
          <SearchInput/>
          <Filter selectedGenres={selectedGenres} setSelectedGenres={setSelectedGenres} />
        </div>
      </Header>
      <SearchContent songs={songs}/>
    </div>
  )
}

export default Search