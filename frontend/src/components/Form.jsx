import React, { useContext, useEffect, useState } from 'react'
import { Input, Typography } from '@material-tailwind/react'
import Button from './Button'
import { UserContext } from 'context/UserContext'
import api from 'api'
import ErrorMessage from './ErrorMessage'
import useAuthModal from 'hooks/useAuthModal'

const Form = ({method}) => {
    const [email, setEmail] = useState('') 
    const [username, setUsername] = useState('') 
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [type, setType] = useState(method)
    const [errorMessage, setErrorMessage] = useState('') 
    const [isSetPreferences, setIsSetPreferences] = useState(false)
    const [loggedIn, setLoggedIn] = useState(false)
    const [, setUserData] = useContext(UserContext)
    const authModal = useAuthModal()

    const submitLogin = async () => {
        try {
            const formData = new FormData() 
            formData.append('username',username) 
            formData.append('password', password)
            const response = await api.post('/auth/token', formData)
            const { access_token, user, preferences } = response.data
            
            setUserData(prevUserData => ({
                ...prevUserData,
                token : access_token,
                user : user
            }))
            
            setLoggedIn(true)
            setErrorMessage("")

            if (preferences) {
                setIsSetPreferences(true)
                authModal.onClose()
            }
            
        } catch (error) {
            console.error("Error logging in: ", error) 
            setErrorMessage(prevErrorMessage => "Incorrect username or password")

        }
    }

    const submitSignup = async () => {
        try {
            const userData = {
                email: email,
                username: username,
                password: password
            }

            const response = await api.post('auth/users', userData)
            if (response.status === 201) {
                // console.log("User created")
                setErrorMessage("User created successfully")
            }
        } catch(error) {
            console.error("Error signing up: ", error)
            setErrorMessage(prevErrorMessage => "Error signing up")
        }
    }
    const handleSubmit = async (e) => {
        e.preventDefault()
        if (type === 'signup') {
            // handle signup
            if (password !== confirmPassword) {
                setErrorMessage("Passwords don't match")
            }
            else {
                await submitSignup()
                await new Promise(resolve => setTimeout(resolve, 2000));
                if (errorMessage!=="Error signing up") {
                    setErrorMessage("")
                    setType('login')
                    authModal.onOpenLogin()
                }
            }
        } else if (type==='login') {
            // handle login
            await submitLogin()
        }
    }

    useEffect(() => {
        if (loggedIn && !isSetPreferences) {
            setErrorMessage('') 
            setType('survey') 
            authModal.onOpenSurvey()
        }
    }, [loggedIn, isSetPreferences, authModal])


    if (type === 'survey') {
        return (
            <form className='mt-8 mb-2 w-full sm:w-96 items-start' >
                <div>yes</div>
            </form>
        )
    }
  
    return (
    <form className='mt-8 mb-2 w-full sm:w-96 items-center' onSubmit={handleSubmit}>
        <ErrorMessage message={errorMessage}/>
        <div className='mb-1
         flex flex-col gap-6'>
            {(type === 'signup') ? (
                <>
                    <Typography variant='h6' color='blue-gray' className='-mb-3 text-white'>
                        Email
                    </Typography>
                    <Input 
                        type='email'
                        size='lg' 
                        placeholder='Your email' 
                        className=" !border-t-blue-gray-200 focus:!border-t-gray-900 bg-neutral-950 border-[1px] border-neutral-400 hover:border-neutral-50" 
                        labelProps={{
                        className: "before:content-none after:content-none"
                        }}
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}  
                    />
                </>
            ) : (
                <></>
            )}
            <Typography variant='h6' color='blue-gray' className='-mb-3 text-white'>
                Username
            </Typography>
            <Input 
                size='lg' 
                placeholder='Your username' 
                className=" !border-t-blue-gray-200 focus:!border-t-gray-900 bg-neutral-950 border-[1px] border-neutral-400 hover:border-neutral-50" 
                labelProps={{
                className: "before:content-none after:content-none"
                }}
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                
            />

            <Typography variant='h6' color='blue-gray' className='-mb-3 text-white'>
                Password
            </Typography>
            <Input 
                type='password'
                size='lg' 
                placeholder='Your password' 
                className=" !border-t-blue-gray-200 focus:!border-t-gray-900 bg-neutral-950 border-[1px] border-neutral-400 hover:border-neutral-50" 
                labelProps={{
                className: "before:content-none after:content-none"
                }}
                value={password} 
                onChange={(e) => setPassword(e.target.value)}
                    
            />

            {(type==="signup") ? (
                <>
                    <Typography variant='h6' color='blue-gray' className='-mb-3 text-white'>
                        Confirm password
                    </Typography>
                    <Input 
                        type='password'
                        size='lg' 
                        placeholder='Confirm your password' 
                        className=" !border-t-blue-gray-200 focus:!border-t-gray-900 bg-neutral-950 border-[1px] border-neutral-400 hover:border-neutral-50" 
                        labelProps={{
                        className: "before:content-none after:content-none"
                        }}
                        value={confirmPassword} 
                        onChange={(e) => setConfirmPassword(e.target.value)} 
                    />                                          
                </>
            ) : (
                <></>
            )}
        </div>
        {(type === "login") ? (
            <Button className="mt-10" type="submit">Log In</Button>
        ) : (
            <Button className="mt-10" type="submit">Sign up</Button>
        )}
        <Typography className='text-center underline mt-5 cursor-pointer hover:text-green-500'>
            {/* TODO: write forgot your password function */}
            Forgot your password?
        </Typography>
        {(type === "login") ? (
            <Typography className='text-center underline mt-2 cursor-pointer hover:text-green-500' onClick={() => {
                setType('signup')
                authModal.onOpenSignup()
            }}>
                Don't have an account? Sign up
            </Typography>
        ) : (
            <Typography className='text-center underline mt-2 cursor-pointer hover:text-green-500' onClick={() => {
                setType('login')
                authModal.onOpenLogin()
            }}>
                Already have an account? Log in 
            </Typography>
        )}
    </form>
  )
}

export default Form