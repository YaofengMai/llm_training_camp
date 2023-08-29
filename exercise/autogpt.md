# AutoGPT与langchain的区别
Langchain的核心提供了prompt template、model、memory、chain、agent等的组件，但需要开发者将它们有机地组织起来，而AutoGPT则是进一步封装，免去开发者的一些工作量。  

AutoGPT突出的是**Autonomous**，而Langchain某种程度上看是一些library，更突出的是它的**Orchestration**能力；前者的目标是直接实现ReAct闭环，而后者在另外一个角度看是framework，可以通过合理的设置使之成为一个Autonomous Agent，拥有类似AutoGPT的能力，当然，也可以做其他的事情。
