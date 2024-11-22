import { UserContext } from 'context/UserContext'
import useAuthModal from 'hooks/useAuthModal'
import React, { useContext, useEffect, useState } from 'react'
import { AiFillHeart, AiOutlineHeart } from 'react-icons/ai'
import { useNavigate } from 'react-router-dom'
import api from 'api'

const LikeButton = ({
    songId
}) => {
    const navigate = useNavigate() 
    const authModal = useAuthModal()
    const [userData, setUserData] = useContext(UserContext)
    const [isLiked, setLiked] = useState(false)

    const Icon = isLiked ? AiFillHeart : AiOutlineHeart

    useEffect(() => {
        if (!userData.user?.id) {
            return
        }

        const fetchData = async () => {
            try {
                const response = await api.post(`/check_like`, {
                    track_id: songId,
                    user_id: userData.user.id
                })
                // console.log(response.data);
                if (response.status === 200) {
                    setLiked(response.data.is_liked)
                }
            } catch (error) {
                console.log(error)
            }
        }
        fetchData()
    }, [songId, userData.user?.id])

    const handleLike = async () => {
        if (!userData.user) {
            return authModal.onOpenLogin()
        }

        if (isLiked) {
            // delete like song
            try {
                const response = await api.post('/unlike_track', {
                    track_id: songId,   
                    user_id: userData.user.id
                })

                if (response.status===200) {
                    setLiked(false)
                }
            } catch (error) {
                console.log(error)
            }
        } else {
            // like song
            try {
                const response = await api.post('/like_track', {
                    track_id: songId,
                    user_id: userData.user.id
                })
                if (response.status===200) { 
                    setLiked(true)
                }
            } catch (error) {
                console.log(error)
            }
        }

    }
  return (
    <button onClick={handleLike} className='hover:opacity-75 transition'>
        <Icon color={isLiked ? "#22c55e" : 'white'} size={25} />
    </button>
  )
}

export default LikeButton