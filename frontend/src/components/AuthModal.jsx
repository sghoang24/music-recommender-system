import React, { useContext, useEffect, useState } from 'react'
import Modal from './Modal'
import Form from './Form'
import useAuthModal from 'hooks/useAuthModal'
import { UserContext } from 'context/UserContext'
import { useNavigate, useLocation } from 'react-router-dom'
import Survey from './Survey'

const AuthModal = () => {
  const navigate = useNavigate()
  const location = useLocation();
  const { onClose, isOpen, method } = useAuthModal()
  const [refreshKey, setRefreshKey] = useState(0)
  const [token] = useContext(UserContext)
  const onChange = (open) => {
    if (!open) {
      onClose()
    }
  }

  useEffect(() => {
    if (token !== "null" && method === "") {
      setRefreshKey((prevKey) => prevKey + 1)
    }

  }, [token])

  useEffect(() => {
    navigate(location.pathname, { replace: true });
    onClose()
  }, [refreshKey, navigate])

  return (
    <>
      {(method==="login") ? (
        <Modal title="Welcome back" description="Login to your account" isOpen={isOpen} onChange={onChange}>
            <Form method={method}/>
        </Modal>
      ) : (method==='signup') ? (
        <Modal title="Welcome back" description="Sign up to start using" isOpen={isOpen} onChange={onChange}>
            <Form method={method}/>
        </Modal>
      ) : (method==='survey') && (
        <Modal title="Welcome back" description="What is your favorite genres?" isOpen={isOpen} onChange={onChange}>
            <Survey/>
        </Modal>
      )}
    </>
  )
}

export default AuthModal