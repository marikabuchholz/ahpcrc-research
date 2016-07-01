





PROGRAM probability_density
  IMPLICIT NONE

  INTEGER :: i, j, ntimesteps, ngridpts, n, k, num_of_elements
  INTEGER, PARAMETER :: out_unit = 50
  REAL :: dx, dt, pi
  COMPLEX :: ii
  REAL, DIMENSION(0:9, 0:9) :: matrix
  REAL, DIMENSION(0:9) :: temp, phi1, phi2, phi3, x
  COMPLEX, DIMENSION(0:9) :: phipast, phicurr, phinext
  dx = 0.1
  dt = 0.1
  pi = 3.141592654
  ntimesteps = 1000
  num_of_elements = 100
  open(unit = out_unit, file = "infwell_results.txt", action = "write", status ="replace")
  DO n = 0, 9
     x(n) = (n + 1.0) / 10.0
  END DO
  dx = 0.01x
  ii = (0., 1.)

  DO i = 0, 9
     DO j = 0, 9
        IF (i == j) THEN
           matrix(i, j) = -2
        ELSE IF (i - j == 1 .OR. i - j == -1) THEN
           matrix(i, j) = 1
        ELSE
           matrix(i, j) = 0
        END IF
     END DO
  END DO
  DO n = 0, 9
     phi1(n) = SQRT(2.0) * SIN(pi * x(n))
     phi2(n) = SQRT(2.0) * SIN(2 * pi * x(n))
     phi3(n) = SQRT(2.0) * SIN(3 * pi * x(n))
     phipast(n) = phipast(n) + phi1(n) + phi2(n) + phi3(n)
     phicurr(n) = phi1(n) * EXP(-1 * pi ** 2 * dt / 2) + phi2(n) * &
     EXP(-1 * 2 ** 2 * pi ** 2 * dt / 2) + phi3(n) * EXP(-1 * (3 * pi) ** 2 * dt / 2) 
  END DO

  DO k = 0, 9
     phinext(k) = 0
  END DO

  DO k = 0, 9
     DO i = 0, 9
        DO j = 0, 9
           temp(i) = temp(i) + matrix(i, j) * phicurr(i)
        END DO
     END DO
  phinext(k) = phipast(k) - ii * 2 * dt * temp(i)
  phipast(k) = phicurr(k)
  phicurr(k) = phinext(k)
  END DO
  DO k = 0, 9
     WRITE(out_unit, *) REAL(CONJG(phicurr(k) * phicurr(k)))
  END DO
END PROGRAM probability_density
