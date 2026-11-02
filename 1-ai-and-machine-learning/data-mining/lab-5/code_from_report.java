// Code extracted from the lab report (report.pdf)

import java.io.FileReader;
import weka.classifiers.functions.SimpleLinearRegression;
import weka.core.Instance;
import weka.core.Instances;

public class Regression {
    public static void main(String args[]) throws Exception {
        Instances data = new Instances(new BufferedReader(new FileReader("D:\\WEKA\\wineData.arff")));
        data.setClassIndex(data.numAttributes() - 1);

        SimpleLinearRegression SimpleLinearRegression = new SimpleLinearRegression();
        SimpleLinearRegression.buildClassifier(data);
        System.out.println(SimpleLinearRegression);

        Instance wine = data.lastInstance();
        double price = SimpleLinearRegression.classifyInstance(wine);
        System.out.println("Wine (+" + wine + "): " + price);
    }
}
