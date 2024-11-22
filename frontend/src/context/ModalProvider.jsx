import AuthModal from '../components/AuthModal'
import React, { useEffect, useState } from 'react'

const ModalProvider = () => {
    const [isMounted, setIsMounted] = useState(false)

    useEffect(() => {
        setIsMounted(true)
    }, [])

    if (!isMounted) {
        return null
    }
  return (
    <>
      <AuthModal />
    </>
  )
}

export default ModalProvider