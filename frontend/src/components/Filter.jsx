import { useState } from 'react'
import { Button as TButton } from '@material-tailwind/react'

const Filter = ({selectedGenres, setSelectedGenres}) => {
    const genres = [
        'All',
        'Pop',
        'Rock',
        'Hip-Hop',
        'Electronic',
        'Jazz',
        'Classical',
        'Country',
        'Instrumental'
    ]
    
    const handleGenreSelect = (genre) => {
        if (genre === 'All') {
            if (selectedGenres.includes('All') && selectedGenres.length === 1) {
                return
            } else if (!selectedGenres.includes('All')) {
                setSelectedGenres(['All'])
                return
            }
        } 
        if (selectedGenres.includes(genre)) {
            if (selectedGenres.length === 1) {
                setSelectedGenres(['All'])
            } else {
                setSelectedGenres(selectedGenres.filter(g => g !== genre))
            }
        } else if (selectedGenres.includes('All')) {
            setSelectedGenres([genre])
        } else {
            setSelectedGenres([...selectedGenres, genre])
        }
    }
  return (
    <div className='w-full flex items-start'>
        {genres.map((genre, index) => (
            <TButton className={`rounded-3xl py-3 mx-2 ${(selectedGenres.includes(genre)) ? ('text-black bg-white hover:bg-white/80') :  ('outline-1 bg-neutral-600 hover:bg-neutral-600/60')}`} onClick={() => handleGenreSelect(genre)}>
                {genre}
            </TButton>
        ))}
        
    </div>
  )
}

export default Filter