/* Conception d'un spport orientable par gravité pour   *
* garder un device avec une face vers le haut           *
* Philippe Rochat, 15 juin 2017                         */

mode_print = false; // True: dispose le pièces à plat pour impression
                   // False: dispose les pièces selon plan de mointage

/* Dimensions principales */
parois=30; // Epaisseur de la parois  de la boite ou sero fixé le système
larg=200; // Largeur intérieur de la boite 
daxes=6; // Diamètre de l'ouverture nécessaire pour passer un axe (en l'occurence un écrou de M5)
epstruct = 3; // Epaisseur des tructures fines (cadres)
deltap = 15; // Distance entre les structures (d au parois pour anneau, puis distance caisse à anneau)
larg_anneau = 30; // Largeur de l'anneau azimutal

/* Paramètre secondaires */
epr=2; // Epaisseur des rondelles

/* Paramètres induits (calculés, ne pas modifier !) */
d_ext_anneau = larg - (2*epr) - (2*deltap);
d_int_anneau = d_ext_anneau - 2*epr;

module rondelle(ext, int, epai) {
    difference() {
        cylinder(d=ext, h=epai, center=true, $fn=50);
        cylinder(d=int, h=epai+0.1, center=true, $fn=100); // Comme c'est un palier parfois, nous forçon une très bonne résolution
    }
}

// Rondelles à l'extérieur, 2x
if(mode_print) {
    translate([-100, 100, epr/2])
        rondelle(daxes+16, daxes, epr);
} else {
        rotate([0,90,0])
            rondelle(daxes+16, daxes, epr);
}

translate([-75, 100, epr/2])
    rondelle(daxes+16, daxes, epr);

// Pallier + rondelle intérieur pour fixation dans la parois, 2x
translate([-50, 100, 0]) {
    translate([0,0,epr/2])
        rondelle(daxes+16, daxes, epr);
    translate([0,0,parois/2])
        rondelle(daxes+2*epstruct, daxes, parois);
}

translate([-25, 100, 0]) {
    translate([0,0,epr/2])
        rondelle(daxes+16, daxes, epr);
    translate([0,0,parois/2])
        rondelle(daxes+2*epstruct, daxes, parois);
}

// Fixation équatoriale avec ... , 1x
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
        translate([0,d_int_anneau/2,(daxes+2*epstruct)/2])
            rotate([90,0,0])
                rondelle(daxes+2*epstruct, daxes, epstruct);
        translate([0,-d_int_anneau/2,(daxes+2*epstruct)/2])
            rotate([90,0,0])
                rondelle(daxes+2*epstruct, daxes, epstruct);
    }

    // We substract 4 axis
    translate([d_ext_anneau/2+40,0,daxes/2+epstruct])
        rotate([0,90,0])
            #cylinder(h=100, d=daxes, center=true);
    translate([-(d_ext_anneau/2+40),0,daxes/2+epstruct])
        rotate([0,90,0])
            #cylinder(h=100, d=daxes, center=true);
    translate([0,d_ext_anneau/2,daxes/2+epstruct])
        rotate([90,0,0])
            #cylinder(h=100, d=daxes, center=true);
    translate([0,-(d_ext_anneau/2),daxes/2+epstruct])
        rotate([90,0,0])
            #cylinder(h=100, d=daxes, center=true);
}


