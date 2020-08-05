import React, { Fragment, useState , useEffect} from "react";
import Grid from "@material-ui/core/Grid";
import CategoryTree from "./CategoryTree";
import ProductGrid from "./ProductGrid";
import { postService } from "../../services/postService";

import { productService } from "../../services/productService";
import { categoryService } from "../../services/categoryService";
import { Page }             from "../../components";

import { subCategoryService } from "../../services/subCategoryService";
import { Typography } from "@material-ui/core";

// import { PostsComponent } from '../posts'

// import { PostsList, PostsDetails } from '../posts/components'

// // import { PostsDetails } from '../posts/post-details'

// function Home() {
//   const [posts, setPosts] = useState([]);
//   const [selectedPost, setSelectedPost] = useState(null);

//   useEffect(() => { 
//     fetch("http://127.0.0.1:8000/api/post/posts", {
//       method:'GET',
//       headers:{
//         'Content-Type': 'application/json',
//         'Authorization':'Token 6165f2762ac4358af1bdfceab20bb75b15d976d6'
//       }
//     })
//     .then(resp => resp.json())
//     .then(resp => setPosts(resp))
//     .catch(error => console.log(error))
//   }, [])

//   const postClicked = post => {
//     setSelectedPost(post);
//     console.log(setSelectedPost.id);
//   }

//   return (
//     <Fragment>
//       <Grid container>
//         <Grid item md={2}>
//          <PostsList posts= {posts} postClicked= {postClicked} /> 
//         </Grid>
//         <Grid item md={10}>
//         <PostsDetails post= {selectedPost}  />
//         </Grid>
//       </Grid>
//     </Fragment>
//   )
// }

// export default Home;
