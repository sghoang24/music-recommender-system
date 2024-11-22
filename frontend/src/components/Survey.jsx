import React, { useContext, useEffect, useState } from 'react'
import { Button as TButton } from '@material-tailwind/react'
import useAuthModal from 'hooks/useAuthModal'
import ErrorMessage from './ErrorMessage'
import api from 'api'
import { UserContext } from 'context/UserContext'

const Survey = () => {
    const [selectedGenres, setSelectedGenres] = useState([])
    const [errorMessage, setErrorMessage] = useState('') 
    const authModal = useAuthModal()
    const [userData, setUserData] = useContext(UserContext)
    const genres = [
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
        if (selectedGenres.includes(genre)) {
            setSelectedGenres(selectedGenres.filter(g => g !== genre))
        } else {
            setSelectedGenres([...selectedGenres, genre])
        
        }
    }
    
    const handleSubmit = async (e) => {
        e.preventDefault()
        if (selectedGenres.length === 0) {
            setErrorMessage("Please select at least one genre")
        }
        try {
            // console.log(userData.token)
            const response = await api.put('/auth/users/preferences', 
                selectedGenres,
                { headers : { Authorization : `Bearer ${userData.token}` } }
            )

            if (response.status === 200) {
                // localStorage.setItem("userPreferences", true)
                const { preferences } = response.data 
                setUserData(prevUserData => ({
                    ...prevUserData,
                    preferences : preferences
                }))
                authModal.onClose()
            }
        } catch (error) {
            console.error(error)
            setErrorMessage("Error updating preferences. Please try again.")
        }
    }

    const laterClicked = () => {
        authModal.onClose()
    }
  return (
    <form className='mt-6 mb-2 w-full sm:w-96' onSubmit={handleSubmit}>
        <ErrorMessage message={errorMessage}/>
        <div className='mt-6 items-start animation-slideIn flex flex-wrap gap-x-4 gap-y-4'>
            {genres.map((genre, index) => (
                <TButton className={`rounded-2xl ${(selectedGenres.includes(genre)) ? ('text-black bg-white hover:bg-white/80') : 'outline-1 bg-neutral-600 hover:bg-neutral-600/60'}`} onClick={() => handleGenreSelect(genre)}>
                    {genre}
                </TButton>
            ))}
        </div>
        <div className='mt-4 p-4 flex justify-end gap-x-4'>
            <TButton className='rounded-2xl bg-white px-3 py-3 disabled:cursor-not-allowed disabled:opacity-50 text-black font-bold hover:opacity-75 transition' onClick={laterClicked}>
                Later 
            </TButton>
            <TButton className='rounded-2xl bg-green-500 border-transparent px-3 py-3 disabled:cursor-not-allowed disabled:opacity-50 text-black font-bold hover:opacity-75 transition' type='submit'>
                Confirm
            </TButton>
        </div>
    </form>
  )
}

export default Survey