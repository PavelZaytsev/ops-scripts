# Cloud Native Corfu Initiative

With the creation of cloud, DevOps and containers came the cloud native world.
The future of computing lies in the cloud-based, containerized, distributed systems,
dynamically managed by automation and orchestration.

### DevOps
The roles of developers and prodops get blurry when it comes to software ownership.
There is a trend of developers doing ops with the help of automation and IaC.

### Infrastructure as Code
With a cloud based approach, tooling, workflows and infrastructure are provisioned by software.
Software should automate every aspect of cloud: infrastructure, applications, monitoring, CI/CD, etc.

### The Coming of Containers
With a cloud based approach came containers.
- They allow standard packaging and distribution format.
- They are lightweight, e.g. transfer of images across the network is fast.
- They are fairly fast, running directly on the real CPU with no virtualization overhead.
- Container environment is application-centric, no need to pull unrelated programs and libraries we don't use.
- Most importantly, container is not only the unit of deployment and packaging, its the unit of reuse,
the same container can bec used as a component of many different services.

![containers](https://i.ibb.co/G5dTHmF/containers.jpg "containers")

### Container Orchestration

- The idea comes from the operating systems
(orchestration is coordination of different activitites in service of a common goal, while).
- Container orchestrator is a single service that takes care of scheduling, orchestration and cluster management.
- The standard for container orchestration did not exist before Kubernetes.

### Kubernetes

- Provides out-of-the-box solution to what have been learned in the DevOps community.
- Automation, failover, centralized logging, monitoring.

![dashboard](https://i.ibb.co/LZ2xzm9/kuber-dash.png "dashboard")

### Cloud Native
- Shorthand way of talking about modern application and services that take advantage of cloud, containers and orchestration as a part of microservice architecture.
- Since we deal with a distributed database, these concepts fit very well with respect to what we do.

### Our Use Cases

![pods](https://i.ibb.co/0Xkwc57/kuber-pods.png "pods")
* Standardized approach to manage the application lifecycle.
    - K8s provides a way to automate all ops part of the development.
* Development, Integration, Staging environments:
    - K8s supports a concept of namespaces.
    - Multiple virtual clusters backed by the physical cluster.
* Different tools available out-of-the-box for CI/CD integrated with k8s environment:
    - Jenkins
    - Gocd
* IaC:
    - All infrastructure and tooling are written in code.
    - Entire Infrastructures can be versioned (helm).
* Monitoring components (demo):
    - Metrics (Prometheus + Grafana):
        - Expose needed metrics via JMX exporter from Corfu.
        - Automatically aggregate metrics.
        - Export metrics into a backed-storage.
        - Query and analyze (Prometheus).
    - Logging (ELK):
        - Aggregate needed logs directly from containers.
        - Automatically aggregate logs in the needed format.
        - Store logs in the persistent storage.
        - Query aggregated logs using the search engine (no grep).
    - Distributed Tracing (Jaeger):
        - Instrument the Corfu code.
        - Trace the requests.
        - Store in the persistent storage.
        - Debug distributed transactions by utilizing context propagation.
    - Helps with:
        - Developer productivity.
        - Complex debugging scenarios.
        - Performance tuning.
        - Distributed testing.
        - Chaos testing.
        - etc.

![monitoring](https://i.ibb.co/HY0LpC1/monitoring.png "monitoring")
