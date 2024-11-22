import React, { createContext, useContext, useEffect, useState } from 'react'
import api from 'api'

export const UserContext = createContext() 

export const UserProvider = (props) => {
    // const [token, setToken] = useState(localStorage.getItem("userToken")) 
    const [userData, setUserData] = useState({
        token : localStorage.getItem("userToken"),
        user: null,
        preferences : localStorage.getItem("userPreferences")   
    })

    useEffect(() => {
        const fetchUser = async() => {
            try {
                // console.log("user context");
                const response = await api.get("/auth/users/me",
                {
                    headers: {
                        Authorization: `Bearer ${userData.token}`
                    }
                })

                if (response.status === 200) {
                    setUserData(u => ({
                        ...u,
                        user: response.data
                    }))
                    localStorage.setItem("userToken", userData.token)
                    localStorage.setItem("userPreferences", response.data.preferences)
                }
            } catch (error) {
                console.error("Error fetching user:", error)
                setUserData({
                    token: null,
                    preferences: null,
                    user: null
                })
                localStorage.setItem("userToken", null) 
                localStorage.setItem("userPreferences", null)
            }
        }
        fetchUser()
    } ,[userData.token, userData.preferences, setUserData])

    return (
        <UserContext.Provider value={[userData, setUserData]}>
            {props.children}
        </UserContext.Provider>
    )
}

export const useUser = () => useContext(UserContext)