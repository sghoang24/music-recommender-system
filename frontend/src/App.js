import './App.css';
import { BrowserRouter, Route, Routes} from 'react-router-dom';
import Layout from './Layout/Layout'
import Home from './Layout/pages/Home';
import Search from 'Layout/pages/Search';
import Liked from 'Layout/pages/Liked';
import Recommend from 'Layout/pages/Recommend';

const App = () => {
  return (
    <BrowserRouter>

      <Routes>
          <Route path='/' element={
            <Layout>
              <Home/>
            </Layout>
          }/>

          <Route path='/search' element={
            <Layout>
              <Search />
            </Layout>
          }/>

          <Route path='/liked' element={
            <Layout>
              <Liked/>
            </Layout>
          }/>

          <Route path='/recommend/:songId' element={
            <Layout>
              <Recommend/>
            </Layout>
          }/>
      </Routes>
    </BrowserRouter>
  );
}

export default App
