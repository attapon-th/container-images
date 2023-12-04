ARG DOCKER_TAG=latest
FROM quay.io/keycloak/keycloak:${DOCKER_TAG} as builder
ARG THEME_JAR=keywind
ARG PREFIX

# Enable health and metrics support
ENV KC_HEALTH_ENABLED=true KC_METRICS_ENABLED=true
ENV KC_HTTP_ENABLED=true KC_HTTP_PORT=8080 KC_HTTP_RELATIVE_PATH=${PREFIX}
ENV KC_FEATURES=preview,docker
ENV KC_DB=postgres

WORKDIR /opt/keycloak
# for demonstration purposes only, please make sure to use proper certificates in production instead
RUN keytool -genkeypair -storepass password -storetype PKCS12 -keyalg RSA -keysize 2048 -dname "CN=server" -alias server -ext "SAN:c=DNS:localhost,IP:127.0.0.1" -keystore conf/server.keystore
RUN /opt/keycloak/bin/kc.sh build

# add theme
# COPY ./${THEME_JAR}.jar /opt/keycloak/providers/${THEME_JAR}.jar

FROM quay.io/keycloak/keycloak:${DOCKER_TAG}
ARG PREFIX

COPY --from=builder /opt/keycloak/ /opt/keycloak/

ENV TZ=Asia/Bangkok
ENV KC_HEALTH_ENABLED=true KC_METRICS_ENABLED=true
ENV KC_HTTP_ENABLED=true KC_HTTP_PORT=8080 KC_HTTP_RELATIVE_PATH=${PREFIX}
ENV KC_FEATURES=preview,docker

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]