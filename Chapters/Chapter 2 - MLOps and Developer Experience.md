# Chapter 2 - MLOps and Developer Experience for Machine Learning

In the last chapter, we delved into the intricacies of GPUs, focusing on drivers, CUDA, and running sample applications. Now, Chapter 2 shifts the focus to the developer experience and operations (MLOps) in machine learning, contrasting it with traditional software development. We aim to provide insights and recommendations on building a practical, efficient workflow for machine learning development.

We will take a bottoms-up approach, starting with the developer first and outlining their day in life in ML workflow. 

## Pre-requisite
This chapter assumes that you have a basic understanding of software development processes and are familiar with fundamental concepts in machine learning.

## Traditional Software Development: A Developer's Perspective

The process of software development has evolved into a well-defined and mature system. The following diagram illustrates the typical flow of traditional software development:

![Software Development Process](Images/developerexperience-1.jpg)


1. **Primary Assets**: In traditional software development, the core assets are the code and its associated configuration settings.

2. **Source Control**: Git often serves as the source of truth, centralizing code and its version history.

3. **Code Review**: Before committing changes, developers typically undergo a code review process, ensuring quality and adherence to standards.

4. **Continuous Integration (CI)**: The CI process plays a crucial role, automatically running tests and building artifacts whenever code changes are made. This step is essential for maintaining code quality and functionality.

5. **Continuous Deployment (CD)**: As changes are approved and merged, CD mechanisms deploy these updates to production. This deployment can be manual or automated, and often employs strategies like feature flags, blue/green deployments, or canary releases to minimize disruptions and ensure stability.

## Machine Learning Development: Data Scientist/Developer Perspective

In contrast to traditional software development, machine learning development introduces unique challenges and complexities. Unlike traditional development, where the primary assets are code and configuration, machine learning development integrates additional critical components like data, model training, evaluation, and deployment.

### Day in the life of an ML engineer
An ML Model is the product. Model is a binary blob (bunch of weights in a compressed form). Model is not an executable. You run the model is the right tool/algorthm that you used to build it. So there is a script to train the model and script to run it. 

#### Data Management and Experimentation
An ML engineer often starts by managing and preprocessing data (e.g. Pandas, NumPy, Spark). This data feeds into building and improving models. So it makes sense to version the data for reproducibility, troubleshooting etc. Depending on the project, the data may be a few MB to TB. For example, DVC (https://dvc.org) is a popular tool for data version control and provides a git-native experience. 

Just like software, Experimentation is a constant routine in ML model development. Jupyter Notebooks are widely used for prototyping and exploratory analysis. But if you have built, tried and tested 100 different models in the last 3 months, how will you track the performance and history? Also how will you reproduce a model if you need to go back? For example, MLflow (https://mlflow.org) open-source platform tracks experiments, logs metrics, and manages models, providing a central hub for ML development.

As the data management and experimentation is an ongoing and repetitive task, it can be automated through Kubeflow pipeline or Airflow, creating reproducible execution steps. This also saves a lot of time from manual errors due to incorrect versions of different softwares (eg. CUDA, Pytorch).

#### Model Training and Hyperparameter Tuning
Model training is an iterative and resource-intensive task. Here, hyperparameter tuning is critical. An ML engineer might set up experiments using tools like Kubeflow Katib for automated hyperparameter optimization. The trained model is saved to model registry. 

#### Model Deployment and Monitoring
Deploying the trained model to production is where CI/CD practices are necessary. Automated pipelines can be set up to handle testing, building, and deploying models. Tools like Jenkins or GitLab CI/CD are often employed to orchestrate these pipelines. For serving models, an ML engineer might use Seldon or Triton Inference Server, which integrate well with Kubernetes for scalable deployment.

Continuous monitoring of deployed models is crucial to ensure performance and reliability. This involves setting up monitoring tools like Prometheus and Grafana to track model performance metrics and system health.

In reality, while almost all product development are embacing ML to certain extent. So it makes a lot of sense to integrate ML development into existing product software development workflow.

### ML Development Process

The following diagram illustrates the typical flow of ML software development.

![Software Development Process](Images/developerexperience-2.jpg)

1. **Data as a Core Asset**: Data is the foundation of any machine learning project. Managing, processing, and versioning data become as crucial as managing code.

2. **Experimentation and Model Training**: Machine learning involves continuous experimentation with models, algorithms, and parameters. This experimentation requires tools and processes to track, manage, and reproduce experiments.

3. **Model Evaluation and Versioning**: Once a model is trained, it must be rigorously evaluated. Managing different versions of models and their performance metrics is a key part of the ML development cycle.

4. **Deployment and Monitoring**: Deploying ML models into production is more complex than traditional software. It involves not just deploying code but also ensuring the model performs as expected in real-world scenarios. Continuous monitoring and retraining become part of the deployment cycle.

### Select Open-source Tools for MLOps

The following table lists a few widely used tools for MLOps on Kubernetes. It is important to emphasize, start with the problems and adopt a tool only if needed.

| Tool           | Complexity         | Use Cases                                                                                      |
|----------------|--------------------|------------------------------------------------------------------------------------------------|
| DVC            | Moderate           | - Version control for large datasets and ML models<br>- Efficient data storage and retrieval<br>- Integration with Git for versioning<br>- Reproducibility of ML experiments<br>- Remote storage management (e.g., S3, GCP)<br>- Support for multiple data versions in ML projects |
| MLflow         | Moderate           | - Tracking and logging of parameters, metrics, and models<br>- ML model lifecycle management<br>- Experiment tracking for reproducibility<br>- Model registry for versioning and management<br>- Deployment of models to various serving environments<br>- Integration with popular ML frameworks (TensorFlow, PyTorch, etc.) |
| Kubeflow       | High               | - End-to-end orchestration of ML workflows on Kubernetes<br>- Scalable pipeline creation and execution<br>- Hyperparameter tuning with Katib<br>- Model serving with TF Serving, PyTorch Serve, etc.<br>- Multi-framework support for diverse ML tasks<br>- Centralized dashboard for managing ML workflows |
| Airflow        | Moderate to High   | - Automation and orchestration of complex workflows<br>- Scheduling and monitoring of ML pipelines<br>- Integration with diverse data sources and ML tools<br>- Dynamic pipeline generation with Python<br>- Customizable and extensible design<br>- Management of task dependencies and execution order |
| Seldon Core    | Moderate to High   | - Scalable deployment of ML models in Kubernetes<br>- Advanced deployment strategies (A/B testing, shadow deployment)<br>- Model monitoring and logging<br>- Rich inference graph with pre/post-processing<br>- Integration with MLflow, Tensorflow, and other frameworks<br>- Custom resource definitions for ML deployments in Kubernetes |


#### How DVC fits into DevOps and MLOps
Integrating DVC with CI/CD creates a robust and reproducible ML development process.

**Developer Interaction:**
* **Easy Integration:** Integrates seamlessly with existing Git workflow.
* **Track files:** Use `dvc add` to track large datasets and model files.
* **Data Versioning:** Create and manage different versions of data and models.
* **Remote Storage:** Connect to cloud storage (AWS S3, Azure Blob Storage, etc.) for data storage.
* **Familiar Experience:** Versioning process similar to Git, making it easy to learn.

**CI/CD Pipelines:**
* **Automates Data and Model Versioning:** Ensures pipelines use correct versions for testing and deployment.
* **Reproducible Workflows:** Guarantees consistent results across pipeline runs.
* **Improved Efficiency:** Automates data and model handling, saving developer time.
* **CI Integration:** Use `dvc pull` to retrieve specific data/model versions for testing.
* **CD Integration:** Use `dvc` to deploy correct version of models with application.

#### How MLflow fits into DevOps and MLOps
MLflow empowers developers to manage their ML projects effectively, fostering experimentation, collaboration, and reliable results.

**Developer Interaction:**
* **Streamlines Workflow:** Provides a centralized platform for managing your entire ML lifecycle.
* **Easy Integration:** Integrate seamlessly with existing projects or start new ones using MLflow templates.
* **Four Key Components:**
    * **MLflow Tracking:** Logs experiments (parameters, code, metrics, outputs) for comparison and visualization.
    * **MLflow Projects:** Packages data science code for reproducibility and sharing.
    * **MLflow Models:** Offers a standard format for model packaging.
    * **Model Registry:** Central repository for versioning and managing models.

**CI/CD Pipelines:**
* **Automates Workflow:** Integrates seamlessly with CI/CD pipelines for automated tracking and deployment.
* **CI Integration:** Log new experiments with every code push, preserving run history.
* **CD Integration:** Automate model deployment from staging to production based on performance or validation.

**Experiment Management:**
* **Log Experiments:** Track all runs with parameters, code versions, metrics, and results.
* **Compare Runs:** Visually compare experiments to understand changes and impact.
* **Reproducible Results:** Track everything for easy replication of past runs.
* **Collaboration:** Share experiments with your team for transparency and efficiency.
* **Centralized Storage:** Keep all experiment data in one place for easy access and analysis.

#### How Kubeflow fits into DevOps and MLOps
Kubeflow offers a comprehensive, Kubernetes-based platform for managing the entire ML lifecycle. It’s particularly beneficial for scalable and complex ML projects, providing flexibility in tooling and infrastructure.

#### Developer Interaction with Kubeflow
- **Installation and Setup:** Begins with setting up Kubeflow on a Kubernetes cluster.
- **Centralized ML Workflow:** Provides a unified interface for managing diverse ML tasks.
- **Pipeline Creation:** Utilize Kubeflow Pipelines for creating and managing end-to-end ML workflows.
- **Jupyter Notebooks:** Offers integrated Jupyter notebooks for interactive development and experimentation.
- **Component Integration:** Seamlessly integrates various components like model training, hyperparameter tuning, and serving.
- **Scalability:** Leverages Kubernetes for scaling ML workflows, suitable for large-scale ML projects.

#### Kubeflow in CI/CD Pipelines
- **Automated Workflows:** Facilitates automation of ML workflows in CI/CD pipelines.
- **Consistent Deployment:** Ensures consistent deployment environments using Kubernetes.
- **Pipeline Versioning:** Tracks different versions of ML pipelines, aiding in reproducibility.
- **Continuous Training:** Supports continuous training paradigms, automatically retraining models with new data.
- **Model Deployment:** Streamlines the deployment process with tools for model serving and monitoring.

#### Managing Experiments with Kubeflow
- **Experiment Tracking:** Track and compare experiments using Kubeflow's UI.
- **Hyperparameter Tuning:** Utilize Katib for automated hyperparameter tuning and optimization.
- **Model Experimentation:** Allows for extensive model experimentation with different frameworks.
- **Pipeline Experimentation:** Supports experimentation with different pipeline configurations.
- **Metrics and Monitoring:** Provides tools for monitoring experiments and gathering key performance metrics.



### Recommendations for ML Development Workflow

Different product teams use ML differently. Some are pure-play ML startups, focusing on building very large language model (LLM), some may just want to finetune a model and run it as an API endpoint. Whereas some others may training a moderate size neural network. While the ML development ecosystem is fairly broad, it is important to be aware of the key problems you need to address for an optimal developer experience.

For those new to machine learning, it's advisable to begin with the bare minimum set of tools and gradually adopt more sophisticated tools and processes as your project's complexity grows. Starting simple helps in understanding the unique aspects of ML development without getting overwhelmed by the vast array of available tools and methodologies. It also depends on your team's expertise on current tools. An opnionated recommendation is as follows.

1. **Start with Data and Model versioning**: You already have code and configuraiton versioning (GIt). Just add model and data versioning with DVC. 

2. **Adopt Advanced Tools purely based on need**: As your project grows, incorporate more advanced tools for experiment tracking and model versioning (MLflow), and automated deployment pipelines (Kubeflow). Likewise, experiment and adopt Ray if you need parallel computing.

