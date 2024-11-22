import React, { useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { twMerge } from 'tailwind-merge'
import { RxCaretLeft, RxCaretRight } from 'react-icons/rx'
import { HiHome } from 'react-icons/hi'
import { BiSearch } from 'react-icons/bi'
import Button from './Button'
import useAuthModal from 'hooks/useAuthModal'
import { UserContext } from 'context/UserContext'
import { FaUserAlt } from 'react-icons/fa'

const Header = ({
  children,
  className
}) => {
  const navigate = useNavigate()
  const authModal = useAuthModal()
  const [userData, setUserData] = useContext(UserContext) 
  const handleLogout = () => {
    // handle logout
    // TODO : call log out api endpoint instead of only handling in frontend
    setUserData(previousUserData => {
      localStorage.setItem("userToken", null)
      return { ...previousUserData, token: null, user: null}})
    // window.location.reload()
  }

  return (
    <div className={twMerge(`
      h-fit bg-gradient-to-b from-emerald-800 p-6
    `, className)}>
      <div className='w-full mb-4 flex items-center justify-between'>
        {/* Desktop view */}
        <div className='hidden md:flex gap-x-2 items-center'>
          {/* button back */}
          <button className='rounded-full bg-black flex items-center justify-center hover:opacity-75 transition' onClick={() => navigate(-1)}>
            <RxCaretLeft size={35} className='text-white'/>
          </button>
          {/* button forward */}
          <button className='rounded-full bg-black flex items-center justify-center hover:opacity-75 transition' onClick={() => navigate(1)}>
            <RxCaretRight size={35} className='text-white'/>
          </button>
        </div>
        {/* Mobile view */}
        <div className='flex md:hidden gap-x-2 items-center'>
          <button className='rounded-full p-2 bg-white flex items-center justify-center hover:opacity-75 transition' onClick={() => navigate('/')}>
            <HiHome className='text-black' size={20}/>
          </button>
          <button className='rounded-full p-2 bg-white flex items-center justify-center hover:opacity-75 transition' onClick={() => navigate('/search')}>
            <BiSearch className='text-black' size={20}/>
          </button>
        </div>
        <div className='flex justify-between items-center gap-x-4'>
          {(userData.token) ? (
            <div className='flex gap-x-4 items-center'>
              <Button onClick={handleLogout} className="bg-white px-6 py-2">
                Logout
              </Button>
              <Button onClick={() => {}} className="bg-white">
                <FaUserAlt/>
              </Button>
            </div>
          ) : (
            <>
              <div>
                <Button className="bg-transparent text-neutral-300 font-medium" onClick={authModal.onOpenSignup}>
                  Sign up
                </Button>
              </div>
              <div>
                <Button className="bg-white px-6 py-2" onClick={authModal.onOpenLogin}>
                  Log in
                </Button>
              </div>
            </>
          )}
        </div>
      </div>
      {children}
    </div>
  )
}

export default Header