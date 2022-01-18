module prism(height=5, length=100){
   rotate([135, 0, 0]){
        difference(){ 
           cube([length, height, height]);

            rotate([45, 0, 0]){    
                cube([length, height*height, height]);
            }
        }
    }
}