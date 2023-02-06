<?php
    /* Location */
    $location = "prediction-algorithm/uploads/uploaded_data_file.csv";
    
    /* Upload file */
    if(move_uploaded_file($_FILES['csv']['tmp_name'], $location)){
        header("Location: index.html");
    }else{
        header("Location: index.html");
    }
?>