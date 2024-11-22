// import React, { useState } from 'react'
import api from 'api'

const getSongs = async () => {
    try {
        const response = await api.get('/get_10_tracks') 

        if (response.status === 200) {
            return response.data
        }
    } catch (error) {
        console.log(error)
        return []
    }
  
}

export default getSongs