// Translate this file with
//
// g++ -O3 --std=c++11 assignment-2019.c -o assignment
//
// Run it with
//
// ./assignment
//
// There should be a result.pvd file that you can open with Paraview.
// Sometimes, Paraview requires to select the representation "Point Gaussian"
// to see something meaningful.
//
// (C) 2018-2019 Tobias Weinzierl

#include <fstream>
#include <sstream>
#include <iostream>
#include <string>
#include <math.h>
#include <limits>
#include <iomanip>


double t          = 0;
double tFinal     = 0;
double tPlot      = 0;
double tPlotDelta = 0;

int snapshotCounter = 0;
int NumberOfBodies = 0;

/**
 * Pointer to pointers. Each pointer in turn points to three coordinates, i.e.
 * each pointer represents one molecule/particle/body.
 */
double** x;

/**
 * Equivalent to x storing the velocities.
 */
double** v;

/**
 * One mass entry per molecule/particle.
 */
double*  mass;

/**
 * Global time step size used.
 */
double   timeStepSize = 0.0;

/**
 * Maximum velocity of all particles.
 */
double   maxV;

/**
 * Minimum distance between two elements.
 */
double   minDx;

/** Forces */
double* force0;
double* force1;
double* force2;

/** Bucketing */
int* bucket;        // Bucket ID of each particle

int NumberOfBuckets = 10;
double* bucketSpeedLimits;
const double vBucket = 200 / NumberOfBuckets;


/**
 * Set up scenario from the command line.
 *
 * This operation is not to be changed in the assignment.
 */
void setUp(int argc, char** argv) {
  NumberOfBodies = (argc-4) / 7;

  x    = new double*[NumberOfBodies];
  v    = new double*[NumberOfBodies];
  mass = new double [NumberOfBodies];

  force0 = new double[NumberOfBodies];
  force1 = new double[NumberOfBodies];
  force2 = new double[NumberOfBodies];

  bucket = new int[NumberOfBodies];
  bucketSpeedLimits = new double[NumberOfBuckets];
  for (int j = NumberOfBuckets - 1; j >= 0; j--) {
    bucketSpeedLimits[j] = (j * vBucket)*(j * vBucket);
  }

  int readArgument = 1;

  tPlotDelta   = std::stof(argv[readArgument]); readArgument++;
  tFinal       = std::stof(argv[readArgument]); readArgument++;
  timeStepSize = std::stof(argv[readArgument]); readArgument++;

  for (int i=0; i<NumberOfBodies; i++) {
    x[i] = new double[3];
    v[i] = new double[3];

    x[i][0] = std::stof(argv[readArgument]); readArgument++;
    x[i][1] = std::stof(argv[readArgument]); readArgument++;
    x[i][2] = std::stof(argv[readArgument]); readArgument++;

    v[i][0] = std::stof(argv[readArgument]); readArgument++;
    v[i][1] = std::stof(argv[readArgument]); readArgument++;
    v[i][2] = std::stof(argv[readArgument]); readArgument++;

    mass[i] = std::stof(argv[readArgument]); readArgument++;

    if (mass[i]<=0.0 ) {
      std::cerr << "invalid mass for body " << i << std::endl;
      exit(-2);
    }
  }

  std::cout << "created setup with " << NumberOfBodies << " bodies" << std::endl;
  
  if (tPlotDelta<=0.0) {
    std::cout << "plotting switched off" << std::endl;
    tPlot = tFinal + 1.0;
  }
  else {
    std::cout << "plot initial setup plus every " << tPlotDelta << " time units" << std::endl;
    tPlot = 0.0;
  }
}


std::ofstream videoFile;


/**
 * This operation is not to be changed in the assignment.
 */
void openParaviewVideoFile() {
  videoFile.open( "result.pvd" );
  videoFile << "<?xml version=\"1.0\"?>" << std::endl
            << "<VTKFile type=\"Collection\" version=\"0.1\" byte_order=\"LittleEndian\" compressor=\"vtkZLibDataCompressor\">" << std::endl
            << "<Collection>";
}





/**
 * This operation is not to be changed in the assignment.
 */
void closeParaviewVideoFile() {
  videoFile << "</Collection>"
            << "</VTKFile>" << std::endl;
}


/**
 * The file format is documented at http://www.vtk.org/wp-content/uploads/2015/04/file-formats.pdf
 *
 * This operation is not to be changed in the assignment.
 */
void printParaviewSnapshot() {
  static int counter = -1;
  counter++;
  std::stringstream filename;
  filename << "result-" << counter <<  ".vtp";
  std::ofstream out( filename.str().c_str() );
  out << "<VTKFile type=\"PolyData\" >" << std::endl
      << "<PolyData>" << std::endl
      << " <Piece NumberOfPoints=\"" << NumberOfBodies << "\">" << std::endl
      << "  <Points>" << std::endl
      << "   <DataArray type=\"Float64\" NumberOfComponents=\"3\" format=\"ascii\">";
//      << "   <DataArray type=\"Float32\" NumberOfComponents=\"3\" format=\"ascii\">";

  for (int i=0; i<NumberOfBodies; i++) {
    out << x[i][0]
        << " "
        << x[i][1]
        << " "
        << x[i][2]
        << " ";
  }

  out << "   </DataArray>" << std::endl
      << "  </Points>" << std::endl
      << " </Piece>" << std::endl
      << "</PolyData>" << std::endl
      << "</VTKFile>"  << std::endl;

  videoFile << "<DataSet timestep=\"" << counter << "\" group=\"\" part=\"0\" file=\"" << filename.str() << "\"/>" << std::endl;
}


/**
 * This is the only operation you are allowed to change in the assignment.
 */
void updateBody() {
  maxV   = 0.0;
  minDx  = std::numeric_limits<double>::max();

  int maxBucket = 0;

  // Sort into buckets
  #pragma omp parallel for reduction(max: maxBucket)
  for (int i = 0; i < NumberOfBodies; i++) {
    const double velocity = v[i][0]*v[i][0] + v[i][1]*v[i][1] + v[i][2]*v[i][2];
    bucket[i] = 0;
    for (int j = NumberOfBuckets - 1; j >= 0; j--) {
      if (velocity >= bucketSpeedLimits[j]) {
        bucket[i] = j;
        maxBucket = std::max(maxBucket, j);
        break;
      }
    }
  }

  for (int bucketNum = 0; bucketNum <= maxBucket; bucketNum++) {
    const int times = 1 << bucketNum;
    const double dt = timeStepSize / ((double) times);

    for (int iterationCount = 0; iterationCount < times; iterationCount++) {
      double iterationMinDx = std::numeric_limits<double>::max();

      #pragma omp parallel for reduction(min: iterationMinDx)
      for (int i = 0; i < NumberOfBodies; i++) {
        if (bucket[i] == bucketNum) {
          double forcex = 0;
          double forcey = 0;
          double forcez = 0;

          for (int j = 0; j < NumberOfBodies; j++) {
            if (i == j) continue;

            const double dx = x[j][0] - x[i][0];
            const double dy = x[j][1] - x[i][1];
            const double dz = x[j][2] - x[i][2];

            const double distance_squared = dx*dx + dy*dy + dz*dz;
            const double distance = std::sqrt(distance_squared);
            const double multiple = mass[j] * mass[i] / (distance_squared * distance);

            // x,y,z forces acting on particle i
            forcex += dx * multiple;
            forcey += dy * multiple;
            forcez += dz * multiple;

            iterationMinDx = std::min(iterationMinDx, distance);
          }

          force0[i] = forcex;
          force1[i] = forcey;
          force2[i] = forcez;
        }
      }

      minDx = std::min(minDx, iterationMinDx);

      #pragma omp simd reduction(max: maxV)
      for (int i = 0; i < NumberOfBodies; i++) {
        if (bucket[i] == bucketNum) {
          x[i][0] += dt * v[i][0];
          x[i][1] += dt * v[i][1];
          x[i][2] += dt * v[i][2];

          v[i][0] += dt * force0[i] / mass[i];
          v[i][1] += dt * force1[i] / mass[i];
          v[i][2] += dt * force2[i] / mass[i];

          maxV = std::max(maxV, v[i][0]*v[i][0] + v[i][1]*v[i][1] + v[i][2]*v[i][2]);
        }
      }

      if (iterationMinDx > 0.01) continue;

      // Object collision
      for (int i = 0; i < NumberOfBodies; i++) {
        if (bucket[i] != bucketNum) continue;

        for (int j = i + 1; j != i && j < NumberOfBodies;) {
          const double dx = x[j][0] - x[i][0];
          const double dy = x[j][1] - x[i][1];
          const double dz = x[j][2] - x[i][2];
          const double distance_squared = dx*dx + dy*dy + dz*dz;

          // No collision, just continue
          if (distance_squared > (0.01*0.01)) {
            j++;
            continue;
          }

          const double denom = mass[i] + mass[j];
          const double weight_i = mass[i] / denom;
          const double weight_j = mass[j] / denom;

          mass[i] = denom;

          x[i][0] = x[i][0] * weight_i + x[j][0] * weight_j;
          x[i][1] = x[i][1] * weight_i + x[j][1] * weight_j;
          x[i][2] = x[i][2] * weight_i + x[j][2] * weight_j;

          v[i][0] = v[i][0] * weight_i + v[j][0] * weight_j;
          v[i][1] = v[i][1] * weight_i + v[j][1] * weight_j;
          v[i][2] = v[i][2] * weight_i + v[j][2] * weight_j;

          x[j] = x[NumberOfBodies - 1];
          v[j] = v[NumberOfBodies - 1];
          bucket[j] = bucket[NumberOfBodies - 1];
          NumberOfBodies--;
        }
      }
    }
  }

  maxV = std::sqrt(maxV);
  t += timeStepSize;
}


/**
 * Main routine.
 *
 * Not to be changed in assignment.
 */
int main(int argc, char** argv) {
  if (argc==1) {
    std::cerr << "usage: " + std::string(argv[0]) + " snapshot final-time dt objects" << std::endl
              << "  snapshot        interval after how many time units to plot. Use 0 to switch off plotting" << std::endl
              << "  final-time      simulated time (greater 0)" << std::endl
              << "  dt              time step size (greater 0)" << std::endl
              << std::endl
              << "Examples:" << std::endl
              << "0.01  100.0  0.001    0.0 0.0 0.0  1.0 0.0 0.0  1.0 \t One body moving form the coordinate system's centre along x axis with speed 1" << std::endl
              << "0.01  100.0  0.001    0.0 0.0 0.0  1.0 0.0 0.0  1.0     0.0 1.0 0.0  1.0 0.0 0.0  1.0  \t One spiralling around the other one" << std::endl
              << "0.01  100.0  0.001    3.0 0.0 0.0  0.0 1.0 0.0  0.4     0.0 0.0 0.0  0.0 0.0 0.0  0.2     2.0 0.0 0.0  0.0 0.0 0.0  1.0 \t Three body setup from first lecture" << std::endl
              << "0.01  100.0  0.001    3.0 0.0 0.0  0.0 1.0 0.0  0.4     0.0 0.0 0.0  0.0 0.0 0.0  0.2     2.0 0.0 0.0  0.0 0.0 0.0  1.0     2.0 1.0 0.0  0.0 0.0 0.0  1.0     2.0 0.0 1.0  0.0 0.0 0.0  1.0 \t Five body setup" << std::endl
              << std::endl
              << "In this naive code, only the first body moves" << std::endl;

    return -1;
  }
  else if ( (argc-4)%7!=0 ) {
    std::cerr << "error in arguments: each planet is given by seven entries (position, velocity, mass)" << std::endl;
    std::cerr << "got " << argc << " arguments (three of them are reserved)" << std::endl;
    std::cerr << "run without arguments for usage instruction" << std::endl;
    return -2;
  }

  std::cout << std::setprecision(15);

  setUp(argc,argv);

  openParaviewVideoFile();

  /* int snapshotCounter = 0; */
  if (t > tPlot) {
    printParaviewSnapshot();
    std::cout << "plotted initial setup" << std::endl;
    tPlot = tPlotDelta;
  }

  int timeStepCounter = 0;
  while (t<=tFinal && NumberOfBodies > 1) {
    updateBody();
    timeStepCounter++;
    if (t >= tPlot) {
      printParaviewSnapshot();
      std::cout << "plot next snapshot"
    		    << ",\t time step=" << timeStepCounter
    		    << ",\t t="         << t
				<< ",\t dt="        << timeStepSize
				<< ",\t v_max="     << maxV
				<< ",\t dx_min="    << minDx
				<< std::endl;

      tPlot += tPlotDelta;
    }
  }

  closeParaviewVideoFile();
  if (NumberOfBodies == 1) {
    std::cout << x[0][0] << "," << x[0][1] << "," << x[0][2] << std::endl;
  }

  return 0;
}
