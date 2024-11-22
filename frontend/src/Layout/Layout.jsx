import React from 'react'
import Sidebar from '../components/Sidebar'
import Player from '../components/Player'

const Layout = ({children}) => {
  return (
    <div>
          {/* <ModalProvider /> */}
      <Sidebar>
        {children}
      </Sidebar>
      <Player/>
    </div>
  )
}

export default Layout

