;
;  Array processing examples using GDL
;
pro display, a, b, f
    compile_opt idl2, logical_predicate
    
    tvscl, a, 0
    tvscl, b, 1
    write_png, 'images/'+f, tvrd()
end

pro arraydemo
    compile_opt idl2, logical_predicate

    window, 0, xs=1024, ys=512

    ; load the images
    i0 = read_png('images/barbara.png')
    i1 = read_png('images/boat.png')
    i2 = read_png('images/cameraman.png')
    i3 = read_png('images/zelda.png')

    ; invert
    display, i2, 255-i2, 'cinvert.png'

    ; alpha-blend
    m03 = bytscl(1.0*i0 + i3)
    m12 = bytscl(1.0*i1 + 2*i2)
    write_png, 'images/bzelda.png', m03 
    write_png, 'images/cboat.png', m12

    ; math
    t = i3/255.0
    m = t^3 - t
    display, i3, m, 'zelda_ghost.png'

    ; filters
    k = [[0,1,0],[-1,0,1],[0,-1,0]]
    im = convol(i1, k)
    display, i1, im, 'boat_edges.png'
    k = [[0,-1,0],[-1,5,-1],[0,-1,0]]
    im = convol(i0, k)
    display, i0, im, 'barbara_sharp.png'
    k = 5*(randomu(seed,3,3)-0.5)
    im = convol(1.0*i2, k)
    display, i2, im, 'camera_random.png'
    print, k
end

