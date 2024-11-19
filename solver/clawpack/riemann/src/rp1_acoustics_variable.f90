! =====================================================
subroutine rp1(maxm,meqn,mwaves,maux,mbc,mx,ql,qr,auxl,auxr,wave,s,amdq,apdq)
! =====================================================

!     # Riemann solver for the acoustics equations in 1d, with
!     #  variable coefficients (heterogeneous media)

! waves:     2
! equations: 2
! aux fields: 2

! Conserved quantities:
!       1 pressure
!       2 velocity

! Auxiliary variables:
!       1 impedance
!       2 sound_speed

!     # auxl(1,i) should contain the impedance Z in cell i
!     # auxl(2,i) should contain the sound speed c in cell i

!     # On input, ql contains the state vector at the left edge of each cell
!     #           qr contains the state vector at the right edge of each cell

!     # On output, wave contains the waves,
!     #            s the speeds,
!     #
!     #            amdq = A^- Delta q,
!     #            apdq = A^+ Delta q,
!     #                   the decomposition of the flux difference
!     #                       f(qr(i-1)) - f(ql(i))
!     #                   into leftgoing and rightgoing parts respectively.
!     #

!     # Note that the i'th Riemann problem has left state qr(:,i-1)
!     #                                    and right state ql(:,i)
!     # From the basic clawpack routines, this routine is called with ql = qr


    implicit double precision (a-h,o-z)

    dimension auxl(maux, 1-mbc:maxm+mbc)
    dimension auxr(maux, 1-mbc:maxm+mbc)
    dimension wave(meqn, mwaves, 1-mbc:maxm+mbc)
    dimension    s(mwaves, 1-mbc:maxm+mbc)
    dimension   ql(meqn, 1-mbc:maxm+mbc)
    dimension   qr(meqn, 1-mbc:maxm+mbc)
    dimension apdq(meqn, 1-mbc:maxm+mbc)
    dimension amdq(meqn, 1-mbc:maxm+mbc)

!     local arrays
!     ------------
    dimension delta(2)


!     # split the jump in q at each interface into waves

!     # find a1 and a2, the coefficients of the 2 eigenvectors:
    do 20 i = 2-mbc, mx+mbc
        delta(1) = ql(1,i) - qr(1,i-1)
        delta(2) = ql(2,i) - qr(2,i-1)

    !        # impedances:
        zi = auxl(1,i)
        zim = auxr(1,i-1)

        a1 = (-delta(1) + zi*delta(2)) / (zim + zi)
        a2 =  (delta(1) + zim*delta(2)) / (zim + zi)
    
    !        # Compute the waves.
    
        wave(1,1,i) = -a1*zim
        wave(2,1,i) = a1
        s(1,i) = -auxr(2,i-1)
    
        wave(1,2,i) = a2*zi
        wave(2,2,i) = a2
        s(2,i) = auxl(2,i)
    
    20 END DO

!     # compute the leftgoing and rightgoing fluctuations:
!     # Note s(1,i) < 0   and   s(2,i) > 0.

    do 220 m=1,meqn
        do 220 i = 2-mbc, mx+mbc
            amdq(m,i) = s(1,i)*wave(m,1,i)
            apdq(m,i) = s(2,i)*wave(m,2,i)
    220 END DO

    return
    end subroutine rp1
