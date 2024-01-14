import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.StringTokenizer;

public class plankLogisticRegression {
	
	public static void main (String[] args) throws IOException {
		double[] theta = new double[35];
		int iterations = 100000;
		double alpha = 2;
		
		ArrayList<ArrayList<Double>> dataPoints = new ArrayList<ArrayList<Double>>();
		BufferedReader br = new BufferedReader(new FileReader("plankingData"));
		String currentLine = br.readLine();
		
		StringTokenizer st;
		
		while (currentLine != null) {
			ArrayList<Double> vector = new ArrayList<Double>();
			currentLine = reduce(currentLine);
			// System.out.println(currentLine);
			
			st = new StringTokenizer(currentLine);
			st.nextToken();
			
			for (int i = 0; i < 36 && st.hasMoreTokens(); i++) {
				vector.add(Double.parseDouble(st.nextToken()));
			}
			currentLine = br.readLine();
			System.out.println(vector);
			dataPoints.add(vector);
		}
		
				
		double m = dataPoints.size();
		double con = -alpha/m;
		
		for (int i = 0; i < iterations; i++) {
			// improve each component
			
			for (int j = 0; j < 35; j++) {
				double change = 0;
				
				for (ArrayList<Double> dataPoint : dataPoints) {
					double[] array = new double[35];
					for (int k = 0; k < 35; k++) array[k] = dataPoint.get(k);
					
					change += -con * dataPoint.get(j) * (dataPoint.get(35) - sigm(dotProduct(theta, array)));
				}
				
				theta[j] -= change;
			}
			
			System.out.printf("Iteration %d: %f\n", i, loss(dataPoints, theta));
		}
		
		
		System.out.println(Arrays.toString(theta));
		
	}
	
	static double loss(ArrayList<ArrayList<Double>> data, double[] theta) {
		double result = 0;
		
		for (int i = 0; i < data.size(); i++) {
			ArrayList<Double> dataPoint = data.get(i);
			double[] array = new double[dataPoint.size()];
			
			for (int j = 0; j < dataPoint.size(); j++) array[j] = dataPoint.get(j);
			
			double localLoss = dataPoint.get(35) * log(sigm(dotProduct(theta, array)));
			localLoss += (1-dataPoint.get(35)) * log((1-sigm(dotProduct(theta, array))));
			
			result += localLoss;
		}
		
		
		int m = data.size();
		
		return -result/m;
	}
	
	
	static double sigm(double z) {
		return 1.0/(1.0 + Math.exp(z));
	}
	
	static double dotProduct(double[] theta, double[] dataPoint) {
		double dot = 0;
		
		
		for (int i = 0; i < 35; i++) {
			dot += theta[i] * dataPoint[i];
		}
		
		return dot;
	}
	
	static String reduce(String s) {
		String out = "";
		
		
		for (int i = 0; i < s.length(); i++) {
			if (s.charAt(i) == '.') {
				out += s.charAt(i);
			} else if (s.charAt(i) >= '0' && s.charAt(i) <= '9') {
				out += s.charAt(i);
			} else if (s.charAt(i) == ' ') {
				out += s.charAt(i);
			}
		}
		
		return out;
	}
	
	static double log(double a) {
		return Math.log(a);
	}
	
}
