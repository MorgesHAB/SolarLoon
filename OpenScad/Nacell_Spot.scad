/* Conception d'un spport orientable par gravité pour   *
* garder un device avec une face vers le haut           *
* Philippe Rochat, 15 juin 2017                         */

mode_print = false; // True: dispose le pièces à plat pour impression
                   // False: dispose les pièces selon plan de mointage avec 
                   // le device en violet

/* Dimensions principales */
parois=30; // Epaisseur de la parois  de la boite ou sero fixé le système
larg=200; // Largeur intérieur de la boite 
daxes=6; // Diamètre de l'ouverture nécessaire pour passer un axe (en l'occurence un écrou de M5)
epstruct = 3; // Epaisseur des tructures fines (cadres)
deltap = 25; // Distance entre les structures (d au parois pour anneau, puis distance caisse à anneau)
larg_anneau = 30; // Largeur de l'anneau azimutal
spot_lo = 68.3;
spot_la = 51.3;
spot_h = 21.4;
sp_dev = 0.5; // interstice entre le device et la nacelle

/* Paramètre secondaires */
epr=2; // Epaisseur des rondelles

/* Paramètres induits (calculés, ne pas modifier !) */
d_ext_anneau = larg - (2*epr) - (2*deltap);
d_int_anneau = d_ext_anneau - 2*epr;
long_entretoise_nacelle = (d_int_anneau-(spot_lo+3*epstruct+2*sp_dev))/2-epstruct;

/****** MODULES pour définir les éléments ******/

// Un cylindre de diametre ext avec un trou de diametre int et une hauteur de epai
module rondelle(ext, int, epai) {
    difference() {
        cylinder(d=ext, h=epai, center=true, $fn=50);
        cylinder(d=int, h=epai+0.1, center=true, $fn=100); // Comme c'est un palier parfois, nous forçon une très bonne résolution
    }
}

// Représentation simplifiée du device spot
module device() {
    color("darkmagenta", 1.0) {
        cube([spot_la, spot_lo, spot_h], center= true);
    }
}

// Entretoise avec collier qui fait pallier pour l'axe dans la parois en styrofoam
module entretoise_collier() {
        translate([0,0,epr/2])
            rondelle(daxes+16, daxes, epr);
        translate([0,0,parois/2])
            rondelle(daxes+2*epstruct, daxes, parois);
}

// Nacelle centrale pour le Spot, en mode montage affiche le device en violet
module nacelle() {
    if(!mode_print) {
       translate([0,0,-spot_h/2+epstruct+0.5]) {
            device();
       }
    }

    difference() {
        cube([spot_la+2*epstruct+2*sp_dev, spot_lo+2*epstruct+2*sp_dev, 2*spot_h], center= true);

        translate([0,0,epstruct]) {
            cube([spot_la+2*sp_dev, spot_lo+2*sp_dev, 2*spot_h], center= true);
        }
      
        translate([spot_la/3+2*epstruct,0,epstruct+1+spot_h]) {
            cube([spot_la/3, spot_lo+4*epstruct+1, 2*spot_h], center= true);
        } 
        translate([-(spot_la/3+2*epstruct),0,epstruct+1+spot_h]) {
            cube([spot_la/3, spot_lo+4*epstruct+1, 2*spot_h], center= true);
        }
        
        translate([0,spot_lo/2+epstruct/2,spot_h-(daxes+2*epstruct)/2]) 
            rotate([90,0,0])
                cylinder(h=4*epstruct, d=daxes, center=true, $fn=100); 
        translate([0,-(spot_lo/2+epstruct/2),spot_h-(daxes+2*epstruct)/2]) 
            rotate([90,0,0])
                cylinder(h=4*epstruct, d=daxes, center=true, $fn=100); 
    }
    
    translate([0,spot_lo/2+epstruct/2,spot_h-(daxes+2*epstruct)/2]) 
        rotate([90,0,0])
            rondelle(daxes+2*epstruct, daxes, 3*epstruct);
    translate([0,-(spot_lo/2+epstruct/2),spot_h-(daxes+2*epstruct)/2]) 
        rotate([90,0,0])
            rondelle(daxes+2*epstruct, daxes, 3*epstruct);
}

// Entrtoise (pallier) pour l'axe entre le disque équatorial et la nacelle
module entretoise(long) {
    rondelle(daxes+2*epstruct, daxes, long);
}


/***** DESSINS DES ELEMENTS *****/
// Rondelles à l'extérieur, 2x
if(mode_print) {
    translate([-100, 100, epr/2])
        rondelle(daxes+16, daxes, epr);
    translate([-75, 100, epr/2])
        rondelle(daxes+16, daxes, epr);
} else {
    translate([d_ext_anneau/2+deltap+3, 0, daxes/2+epstruct])
        rotate([0,90,0])
            rondelle(daxes+16, daxes, epr);
    translate([-(d_ext_anneau/2+deltap+3), 0, daxes/2+epstruct])
        rotate([0,90,0])
            rondelle(daxes+16, daxes, epr);    
}



// Pallier + rondelle intérieur pour fixation dans la parois, 2x
if(mode_print) {
    translate([-50, 100, 0]) 
        entretoise_collier();

    translate([-25, 100, 0]) {
        entretoise_collier();

    }
} else {
     translate([d_ext_anneau/2+deltap+3+parois+3, 0, daxes/2+epstruct]) {
        rotate([0,-90,0]) 
            entretoise_collier();
    }
    translate([-(d_ext_anneau/2+deltap+3+parois+3), 0, daxes/2+epstruct]) {
        rotate([0,90,0]) 
            entretoise_collier();
    }
}

// Anneau equatorial, 1x. Print and no print mode is same
difference() {
    union() {
        translate([0,0,larg_anneau/2])
            rondelle(d_ext_anneau, d_ext_anneau-(2*epr), larg_anneau);
        // 2 paliers sur la nacelle, extérieur
        translate([d_ext_anneau/2+(deltap/2-0.5),0,(daxes+2*epstruct)/2])
            rotate([0,90,0])
                rondelle(daxes+2*epstruct, daxes, deltap); // equiv: rondelle(daxes+2*epstruct, daxes, (larg-(2*epr)-d_ext_anneau)/2);
        translate([-(d_ext_anneau/2+(deltap/2-0.5)),0,(daxes+2*epstruct)/2])
            rotate([0,90,0])
                rondelle(daxes+2*epstruct, daxes, deltap);
        // 2 paliers sur la boite intérieure
        translate([0,d_int_anneau/2,larg_anneau-(daxes+2*epstruct)/2])
            rotate([90,0,0])
                rondelle(daxes+2*epstruct, daxes, epstruct);
        translate([0,-d_int_anneau/2,larg_anneau-(daxes+2*epstruct)/2])
            rotate([90,0,0])
                rondelle(daxes+2*epstruct, daxes, epstruct);
    }

    // We substract 4 axis
    translate([d_ext_anneau/2+40,0,daxes/2+epstruct])
        rotate([0,90,0])
            if(mode_print) {
                cylinder(h=100, d=daxes, center=true);
            } else {
                #cylinder(h=100, d=daxes, center=true);
            }
    translate([-(d_ext_anneau/2+40),0,daxes/2+epstruct])
        rotate([0,90,0])
            if(mode_print) {
                cylinder(h=100, d=daxes, center=true);
            } else {
                #cylinder(h=100, d=daxes, center=true);
            }
            
    translate([0,d_ext_anneau/2,larg_anneau-(daxes/2+epstruct)])
        rotate([90,0,0])
            if(mode_print) {            
                cylinder(h=100, d=daxes, center=true);
            } else {
                #cylinder(h=100, d=daxes, center=true);
            }
    translate([0,-(d_ext_anneau/2),larg_anneau-(daxes/2+epstruct)])
        rotate([90,0,0])
            if(mode_print) {
                cylinder(h=100, d=daxes, center=true);
            } else {
                #cylinder(h=100, d=daxes, center=true);
            }
}



if(mode_print) {
    translate([0,0,spot_h])
        nacelle();
} else {
    translate([0,0,spot_h-(daxes+2*epstruct)/2+larg_anneau-(daxes/2+epstruct)])
        rotate([0,180,0])
            nacelle();
}



if(mode_print) {
    translate([-100, 70, long_entretoise_nacelle/2])
        entretoise(long_entretoise_nacelle);
    translate([-100, 40, long_entretoise_nacelle/2])
    entretoise(long_entretoise_nacelle);
} else {
    translate([0,spot_lo/2+2*epstruct+long_entretoise_nacelle/2+0.25,larg_anneau-(daxes/2+epstruct)])
        rotate([90,0,0])
            entretoise(long_entretoise_nacelle);
    translate([0,-(spot_lo/2+2*epstruct+long_entretoise_nacelle/2+0.25),larg_anneau-(daxes/2+epstruct)])
        rotate([90,0,0])
            entretoise(long_entretoise_nacelle);
}






